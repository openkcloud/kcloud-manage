#!/bin/bash

# AI SOFTWARE IDE Backend 배포 스크립트

echo "🚀 AI SOFTWARE IDE Backend 배포를 시작합니다..."

# 네임스페이스 생성
echo "📦 네임스페이스 생성 중..."
kubectl apply -f k8s-namespace.yaml

# ServiceAccount 및 RBAC 설정
echo "🔐 ServiceAccount 및 RBAC 설정 중..."
kubectl apply -f k8s-serviceaccount.yaml

# ConfigMap 및 Secret 생성
echo "⚙️  ConfigMap 및 Secret 생성 중..."
kubectl apply -f k8s-configmap.yaml

# Docker 이미지 빌드
echo "🐳 Docker 이미지 빌드 중..."
cd backend
docker build -t ai-sw-ide-backend:latest .
cd ..

# Deployment 및 Service 배포
echo "🚀 Deployment 및 Service 배포 중..."
kubectl apply -f k8s-deployment.yaml

# 배포 상태 확인
echo "✅ 배포 상태 확인 중..."
kubectl get pods -n ai-sw-ide -l app=ai-sw-ide-backend

echo "🎉 AI SOFTWARE IDE Backend 배포가 완료되었습니다!"
echo "📝 서비스 확인: kubectl get svc -n ai-sw-ide"
echo "📝 로그 확인: kubectl logs -n ai-sw-ide -l app=ai-sw-ide-backend" 