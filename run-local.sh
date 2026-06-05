#!/bin/bash
# Quick script to run the dashboard container locally for testing

IMAGE_NAME="thoughts-dashboard:latest"

echo "Starting thoughts dashboard container..."
echo ""

# Run using podman (or docker if available)
if command -v podman &> /dev/null; then
    podman run --rm -it \
        -p 5000:5000 \
        --name thoughts-dashboard \
        ${IMAGE_NAME}
elif command -v docker &> /dev/null; then
    docker run --rm -it \
        -p 5000:5000 \
        --name thoughts-dashboard \
        ${IMAGE_NAME}
else
    echo "Error: Neither podman nor docker found. Please install one of them."
    exit 1
fi
