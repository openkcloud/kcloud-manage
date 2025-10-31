#!/bin/bash

set -e

# 변수 설정
IMAGE_NAME="ai-sw-ide-frontend"
IMAGE_TAG=${1:-"latest"}
REGISTRY=${2:-"localhost:5000"}  # 로컬 레지스트리 사용시
NAMESPACE="monitoring"

echo "🚀 AI SOFTWARE IDE Frontend 빌드 및 배포 시작..."

# 1. Docker 이미지 빌드
echo "📦 Docker 이미지 빌드 중..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# 2. 레지스트리에 이미지 푸시 (필요시)
if [ "$REGISTRY" != "local" ]; then
    echo "📤 이미지를 레지스트리에 푸시 중..."
    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
    docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
    
    # deployment.yaml에서 이미지 업데이트
    sed -i "s|image: ai-sw-ide-frontend:latest|image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g" k8s/deployment.yaml
fi

# 3. Kubernetes 네임스페이스 생성 (없는 경우)
echo "🔧 네임스페이스 확인 및 생성..."
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

# 4. Kubernetes 리소스 배포
echo "🚢 Kubernetes에 배포 중..."
kubectl apply -k k8s/

# 5. 배포 상태 확인
echo "✅ 배포 상태 확인 중..."
kubectl rollout status deployment/ai-sw-ide-frontend -n ${NAMESPACE}

# 6. 서비스 정보 출력
echo "📋 서비스 정보:"
kubectl get svc -n ${NAMESPACE} | grep ai-sw-ide-frontend

echo "🎉 배포 완료!"
echo "💡 외부에서 접근하려면 NodePort 30080을 사용하세요." 