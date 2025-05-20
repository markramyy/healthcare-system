#!/bin/bash

# Start minikube
minikube start

# Build the Docker image
docker build -t healthcare-system:latest .

# Apply the Kubernetes secrets
kubectl apply -f k8s/secrets.yaml

# Apply the Kubernetes manifests
kubectl apply -k k8s/overlays/dev

# Start the application
minikube service web -n healthcare-dev --url
