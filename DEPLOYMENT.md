# Deployment Guide - Thoughts Dashboard

## Quick Deployment Steps

### 1. Build the Container Image

```bash
./build.sh
```

Or manually:
```bash
podman build -t thoughts-dashboard:latest -f Containerfile .
```

### 2. Test Locally (Optional)

```bash
podman run -p 5000:5000 thoughts-dashboard:latest
```

Visit http://localhost:5000 to verify the dashboard works.

### 3. Push to Container Registry

Replace `<registry>` and `<namespace>` with your values:

```bash
# Tag the image
podman tag thoughts-dashboard:latest <registry>/<namespace>/thoughts-dashboard:latest

# Login to registry
podman login <registry>

# Push the image
podman push <registry>/<namespace>/thoughts-dashboard:latest
```

Example for OpenShift internal registry:
```bash
podman tag thoughts-dashboard:latest image-registry.openshift-image-registry.svc:5000/thoughts-app/thoughts-dashboard:latest
podman push image-registry.openshift-image-registry.svc:5000/thoughts-app/thoughts-dashboard:latest
```

### 4. Update Kubernetes Deployment

Edit `kubernetes-deployment.yaml` and update the image reference:

```yaml
image: <registry>/<namespace>/thoughts-dashboard:latest
```

### 5. Deploy to Cluster

```bash
# Apply the deployment
kubectl apply -f kubernetes-deployment.yaml

# Or using oc (OpenShift)
oc apply -f kubernetes-deployment.yaml
```

### 6. Verify Deployment

```bash
# Check pod status
kubectl get pods -l app=thoughts-dashboard

# Check service
kubectl get svc thoughts-dashboard

# Check route (OpenShift)
oc get route thoughts-dashboard

# View logs
kubectl logs -f deployment/thoughts-dashboard
```

### 7. Access the Dashboard

For OpenShift:
```bash
# Get the route URL
oc get route thoughts-dashboard -o jsonpath='{.spec.host}'
```

For Kubernetes with port-forward:
```bash
kubectl port-forward svc/thoughts-dashboard 5000:5000
# Access at http://localhost:5000
```

## Architecture

- **Base Image**: Python 3.8-slim
- **Application Port**: 5000
- **User**: Non-root user (UID 1001)
- **Database**: Connects to postgresql.thoughts-app.svc.cluster.local

## Resource Requirements

- **Memory Request**: 128Mi
- **Memory Limit**: 256Mi
- **CPU Request**: 100m
- **CPU Limit**: 500m

## Health Checks

- **Liveness Probe**: HTTP GET / on port 5000 (every 30s)
- **Readiness Probe**: HTTP GET / on port 5000 (every 10s)

## Scaling

To scale the deployment:

```bash
kubectl scale deployment thoughts-dashboard --replicas=3
```

## Updating the Application

1. Make code changes
2. Rebuild image with new tag:
   ```bash
   ./build.sh v1.1
   ```
3. Push new image to registry
4. Update image tag in kubernetes-deployment.yaml
5. Apply changes:
   ```bash
   kubectl apply -f kubernetes-deployment.yaml
   ```

Or use rolling update:
```bash
kubectl set image deployment/thoughts-dashboard dashboard=<registry>/<namespace>/thoughts-dashboard:v1.1
```

## Troubleshooting

### Pod not starting
```bash
# Check pod events
kubectl describe pod -l app=thoughts-dashboard

# Check logs
kubectl logs -l app=thoughts-dashboard
```

### Database connection issues
```bash
# Test DNS resolution from pod
kubectl exec -it deployment/thoughts-dashboard -- nslookup postgresql.thoughts-app.svc.cluster.local

# Check database connectivity
kubectl exec -it deployment/thoughts-dashboard -- python -c "import psycopg2; conn = psycopg2.connect(host='postgresql.thoughts-app.svc.cluster.local', database='thoughts', user='thoughts', password='thoughts123'); print('Connected!')"
```

### View application logs
```bash
# Stream logs
kubectl logs -f deployment/thoughts-dashboard

# Last 100 lines
kubectl logs --tail=100 deployment/thoughts-dashboard
```

## Environment Variables

To customize database connection, add environment variables to the deployment:

```yaml
env:
- name: DB_HOST
  value: "postgresql.thoughts-app.svc.cluster.local"
- name: DB_NAME
  value: "thoughts"
- name: DB_USER
  value: "thoughts"
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-credentials
      key: password
```

Then update app.py to read from environment variables.

## Security Considerations

1. **Admin Panel**: Currently accessible to all users. Consider adding:
   - Authentication (basic auth, OAuth, etc.)
   - Network policies to restrict access
   - Read-only mode for non-admin users

2. **Database Credentials**: Currently hardcoded. Recommend:
   - Use Kubernetes Secrets
   - Or use environment variables from ConfigMap/Secret

3. **HTTPS**: The Route is configured for TLS edge termination

## Production Checklist

- [ ] Image pushed to registry
- [ ] Database credentials secured (use Secrets)
- [ ] Resource limits configured appropriately
- [ ] Health checks working
- [ ] Admin panel access restricted
- [ ] HTTPS/TLS enabled
- [ ] Monitoring/logging configured
- [ ] Backup strategy for database
