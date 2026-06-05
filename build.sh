#!/bin/bash
# Build script for thoughts dashboard container

IMAGE_NAME="thoughts-dashboard"
IMAGE_TAG="${1:-latest}"

echo "Building container image: ${IMAGE_NAME}:${IMAGE_TAG}"

# Build using podman (or docker if available)
if command -v podman &> /dev/null; then
    podman build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Containerfile .
elif command -v docker &> /dev/null; then
    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Containerfile .
else
    echo "Error: Neither podman nor docker found. Please install one of them."
    exit 1
fi

echo ""
echo "Build complete! Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
echo "To run locally:"
echo "  podman run -p 5000:5000 ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
echo "To push to registry:"
echo "  podman tag ${IMAGE_NAME}:${IMAGE_TAG} <registry>/<namespace>/${IMAGE_NAME}:${IMAGE_TAG}"
echo "  podman push <registry>/<namespace>/${IMAGE_NAME}:${IMAGE_TAG}"
