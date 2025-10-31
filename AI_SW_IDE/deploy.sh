#!/bin/bash

# AI SOFTWARE IDE Backend Deployment Script

echo "🚀 Starting AI SOFTWARE IDE Backend deployment..."

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f k8s-namespace.yaml

# ServiceAccount and RBAC setup
echo "🔐 Setting up ServiceAccount and RBAC..."
kubectl apply -f k8s-serviceaccount.yaml

# Create ConfigMap and Secret
echo "⚙️  Creating ConfigMap and Secret..."
kubectl apply -f k8s-configmap.yaml

# Build Docker image
echo "🐳 Building Docker image..."
cd backend
docker build -t ai-sw-ide-backend:latest .
cd ..

# Deploy Deployment and Service
echo "🚀 Deploying Deployment and Service..."
kubectl apply -f k8s-deployment.yaml

# Check deployment status
echo "✅ Checking deployment status..."
kubectl get pods -n ai-sw-ide -l app=ai-sw-ide-backend

echo "🎉 AI SOFTWARE IDE Backend deployment completed!"
echo "📝 Check service: kubectl get svc -n ai-sw-ide"
echo "📝 Check logs: kubectl logs -n ai-sw-ide -l app=ai-sw-ide-backend" 