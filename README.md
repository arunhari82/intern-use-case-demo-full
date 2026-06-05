# Thoughts Database Dashboard

A simple Flask web dashboard for viewing thoughts database reporting.

## Requirements

- Python 3.8
- PostgreSQL database access

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

```bash
python app.py
```

The dashboard will be available at: http://localhost:5000

## Features

### Main Dashboard (/)
- View all thoughts with ratings and status
- Summary statistics (total thoughts, approved, rejected, etc.)
- Display similarity scores from AI evaluations
- Filter thoughts by status (All, Approved, Rejected, In Review, Removed)
- Clean, modern UI with color-coded status badges
- Real-time data from PostgreSQL database

### Admin Panel (/admin)
- Execute custom SQL queries directly from the web interface
- View query results in formatted tables
- Pre-loaded example queries for common debugging tasks
- Supports SELECT, INSERT, UPDATE, DELETE statements
- No SSH access required for database debugging

## Database Configuration

The app connects to:
- Host: postgresql.thoughts-app.svc.cluster.local
- Database: thoughts
- Username: thoughts
- Password: thoughts123

To change these settings, edit the `DB_CONFIG` dictionary in `app.py`.

## Pages

### Main Dashboard (/)

1. **Summary Stats**: Overview cards showing total counts and ratings
2. **Status Filter**: Dropdown to filter thoughts by status with live count
3. **Thoughts Table**: Detailed table with:
   - Content of each thought
   - Author and biography
   - Status (APPROVED, REJECTED, IN_REVIEW, REMOVED)
   - Thumbs up/down counts
   - Net rating (thumbs up - thumbs down)
   - AI similarity score
   - Creation timestamp

### Admin Panel (/admin)

1. **SQL Query Editor**: Large textarea for writing custom SQL queries
2. **Quick Actions**: 
   - Run Query button
   - Clear button
3. **Example Queries**: Click-to-use common queries:
   - View all thoughts
   - Count by status
   - Top authors by rating
   - Thoughts with similarity scores
   - Approved thoughts statistics
4. **Query Results**: Dynamic table showing results with:
   - All columns from your SELECT statement
   - Row count
   - Scrollable results
   - Success/error messages

## URLs

- Main Dashboard: http://localhost:5000/
- Admin Panel: http://localhost:5000/admin

## Deployment

For containerized deployment to Kubernetes/OpenShift, see [DEPLOYMENT.md](DEPLOYMENT.md).

Quick deploy:
```bash
# Build container
./build.sh

# Deploy to cluster
kubectl apply -f kubernetes-deployment.yaml
```
