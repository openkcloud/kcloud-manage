#!/bin/bash

set -e

# Variable settings
IMAGE_NAME="ai-sw-ide-frontend"
IMAGE_TAG=${1:-"latest"}
REGISTRY=${2:-"localhost:5000"}  # For local registry usage
NAMESPACE="monitoring"

echo "🚀 Starting AI SOFTWARE IDE Frontend build and deployment..."

# 1. Build Docker image
echo "📦 Building Docker image..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# 2. Push image to registry (if needed)
if [ "$REGISTRY" != "local" ]; then
    echo "📤 Pushing image to registry..."
    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
    docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
    
    # Update image in deployment.yaml
    sed -i "s|image: ai-sw-ide-frontend:latest|image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml
fi

# 3. Create Kubernetes namespace (if it doesn't exist)
echo "🔧 Checking and creating namespace..."
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# 4. Deploy Kubernetes resources
echo "🚢 Deploying to Kubernetes..."
kubectl apply -k k8s/

# 5. Check deployment status
echo "✅ Checking deployment status..."
kubectl rollout status deployment/ai-sw-ide-frontend -n ${NAMESPACE}

# 6. Print service information
echo "📋 Service information:"
kubectl get svc -n ${NAMESPACE} | grep ai-sw-ide-frontend

echo "🎉 Deployment completed!"
echo "💡 Use NodePort 30080 to access externally." 