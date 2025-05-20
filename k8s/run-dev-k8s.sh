#!/bin/bash

# Exit on error
set -e

echo "🚀 Deploying to development environment..."

# Start minikube
minikube start

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t healthcare-system:latest .

# Apply the Kubernetes secrets
echo "🔐 Applying Kubernetes secrets..."
kubectl apply -f k8s/secrets.yaml

# Apply the Kubernetes manifests
echo "⚙️ Applying Kubernetes manifests..."
kubectl apply -k k8s/overlays/dev

# Start the application
echo "🚀 Starting application..."
minikube service web -n healthcare-dev --url
