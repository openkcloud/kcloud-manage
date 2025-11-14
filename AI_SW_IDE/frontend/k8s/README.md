# AI Software IDE Frontend - Kubernetes 배포

이 디렉토리는 GPU Dashboard Frontend를 Kubernetes에 배포하기 위한 매니페스트 파일들을 포함합니다.

## 주요 변경사항

### ConfigMap으로 분리된 설정
- **API_URL**: 백엔드 API 서버 URL
- **nginx.conf**: Nginx 설정 파일

### 런타임 환경변수 주입
- 빌드 후에도 환경변수 변경 가능
- `config.js.template`을 사용하여 런타임에 환경변수 주입

## 파일 구조

```
k8s/
├── configmap.yaml      # ConfigMap 설정
├── deployment.yaml     # Deployment 설정
├── service.yaml        # Service 설정 (ClusterIP + NodePort)
├── kustomization.yaml  # Kustomize 설정
└── README.md          # 이 파일
```

## 배포 방법

### 1. 수동 배포

```bash
# 네임스페이스 생성
kubectl create namespace monitoring

# 모든 리소스 배포
kubectl apply -k k8s/

# 배포 상태 확인
kubectl rollout status deployment/gpu-dashboard-frontend -n monitoring
```

### 2. 스크립트를 사용한 배포

```bash
# 로컬 이미지 사용
./scripts/build-and-deploy.sh

# 특정 태그와 레지스트리 사용
./scripts/build-and-deploy.sh v1.0.0 your-registry.com
```

## 설정 변경

### API URL 변경
```bash
kubectl patch configmap gpu-dashboard-frontend-config -n monitoring \
  --patch '{"data":{"API_URL":"http://new-api-url:8000"}}'

# Pod 재시작으로 변경사항 적용
kubectl rollout restart deployment/gpu-dashboard-frontend -n monitoring
```

### Nginx 설정 변경
```bash
kubectl edit configmap gpu-dashboard-frontend-config -n monitoring
# nginx.conf 부분을 수정 후 저장

# Pod 재시작
kubectl rollout restart deployment/gpu-dashboard-frontend -n monitoring
```

## 접근 방법

### 클러스터 내부에서 접근
```
http://gpu-dashboard-frontend-svc.monitoring.svc.cluster.local
```

### 외부에서 접근
```
http://<NODE_IP>:30080
```

## 모니터링

### Pod 상태 확인
```bash
kubectl get pods -n monitoring -l app=gpu-dashboard-frontend
```

### 로그 확인
```bash
kubectl logs -f deployment/gpu-dashboard-frontend -n monitoring
```

### 서비스 상태 확인
```bash
kubectl get svc -n monitoring | grep gpu-dashboard-frontend
```

## 문제 해결

### 1. Pod가 시작되지 않는 경우
```bash
kubectl describe pod <pod-name> -n monitoring
kubectl logs <pod-name> -n monitoring
```

### 2. 환경변수가 제대로 주입되지 않는 경우
```bash
# Pod 내부에서 환경변수 확인
kubectl exec -it <pod-name> -n monitoring -- env | grep API_URL

# config.js 파일 확인
kubectl exec -it <pod-name> -n monitoring -- cat /usr/share/nginx/html/config.js
```

### 3. 백엔드 연결 문제
- ConfigMap의 API_URL이 올바른지 확인
- 백엔드 서비스가 실행 중인지 확인
- 네트워크 정책이 통신을 차단하지 않는지 확인

## 리소스 정리

```bash
# 모든 리소스 삭제
kubectl delete -k k8s/

# 또는 개별 삭제
kubectl delete deployment gpu-dashboard-frontend -n monitoring
kubectl delete service gpu-dashboard-frontend-svc gpu-dashboard-frontend-nodeport -n monitoring
kubectl delete configmap gpu-dashboard-frontend-config -n monitoring
``` 