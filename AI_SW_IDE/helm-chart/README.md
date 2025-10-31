# AI SOFTWARE IDE Helm Chart

이 Helm 차트는 AI SOFTWARE IDE 애플리케이션을 Kubernetes 클러스터에 배포합니다.

## 구성 요소

- **Backend**: FastAPI 기반 백엔드 API 서버
- **Frontend**: React 기반 프론트엔드 웹 애플리케이션  
- **Data Observer**: NFS 볼륨 데이터 모니터링 서비스
- **PostgreSQL**: 데이터베이스 (Bitnami 차트 사용)

## 설치 전 요구사항

- Kubernetes 1.19+
- Helm 3.2.0+
- PV 프로비저너 (영구 볼륨용)
- NFS 서버 (Data Observer용)

## 환경별 설정

AI SOFTWARE IDE는 환경별로 달라질 수 있는 설정들을 `global.environment` 섹션에서 중앙 관리합니다.

### 주요 환경 설정

```yaml
global:
  environment:
    # NFS 서버 설정
    nfs:
      address: "<YOUR_NFS_SERVER_IP>"
    
    # Kubernetes 워커 노드명
    nodes:
      workers: "<YOUR_WORKER_NODE_NAMES>(comma-separated: e.g. k8s-worker-1,k8s-worker-2)"
    
    # 외부 서비스 URL
    services:
      prometheus: "<YOUR_PROMETHEUS_ADDRESS>"
      redis: "redis://<YOUR_REDIS_HOST>:6379/0"
    
    # CORS 설정
    cors:
      origins: "http://ai-sw-ide-frontend.ai-sw-ide.svc.cluster.local:4000,http://localhost:4000,http://127.0.0.1:4000"
    
    # 애플리케이션 설정
    app:
      logLevel: "INFO"
      gpuFetchInterval: "30"
      secretAlgorithm: "HS256"
      secretKey: "okestro"
```

### 환경별 설정 변경 방법

1. **values.yaml 직접 수정**
   ```bash
   vi values.yaml
   # global.environment 섹션 수정
   ```

2. **Helm install 시 오버라이드**
   ```bash
   helm install ai-sw-ide . \
     --set global.environment.nfs.address="<YOUR_NFS_SERVER_IP>" \
     --set global.environment.nodes.workers="<YOUR_WORKER_NODE_NAMES>"
   ```

3. **별도 values 파일 사용**
   ```bash
   # production-values.yaml 생성
   echo "
   global:
     environment:
       nfs:
         address: 'prod-nfs-server.company.com'
       nodes:
         workers: 'prod-worker-1,prod-worker-2,prod-worker-3'
   " > production-values.yaml
   
   helm install ai-sw-ide . -f production-values.yaml
   ```

## 빠른 시작

### 1. 이 폴더로 이동
```bash
cd helm-chart
```

### 2. 원클릭 배포
```bash
./quick-start.sh
```

**AI SOFTWARE IDE Deployment Tool**은 다음 기능을 제공합니다:
- 🔍 **환경 검증**: kubectl, helm 설치 및 클러스터 접근 확인
- 🏷️  **네임스페이스 관리**: 자동 감지 및 생성
- 📦 **의존성 해결**: Helm 리포지토리 및 차트 의존성 자동 처리
- 🚀 **원클릭 배포**: 진행 상황 표시와 함께 완전 자동화된 배포
- 📊 **상태 검증**: 배포 후 모든 Pod 상태 실시간 확인
- 📋 **접근 정보**: 서비스 접근 URL 및 관리 명령어 자동 생성

## 수동 설치

### 1. Helm 리포지토리 추가
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### 2. 의존성 업데이트
```bash
helm dependency update
```

### 3. 설치
```bash
helm install ai-sw-ide . -n ai-sw-ide --create-namespace
```

### 4. 커스텀 값으로 설치
```bash
helm install ai-sw-ide . -n ai-sw-ide --create-namespace -f custom-values.yaml
```

## 설정

### 주요 설정 값

```yaml
# 글로벌 설정
global:
  imageRegistry: ""
  namespace: ai-sw-ide

# 백엔드 설정
backend:
  enabled: true
  image:
    repository: ai-sw-ide/backend
    tag: "latest"
  service:
    type: NodePort
    port: 8000
    nodePort: 30800
  env:
    - name: DATABASE_URL
      value: "postgresql://<DB_USER>:<DB_PASSWORD>@ai-sw-ide-postgresql:5432/ai-sw-ide"

# 프론트엔드 설정  
frontend:
  enabled: true
  image:
    repository: ai-sw-ide/frontend
    tag: "latest"
  service:
    type: NodePort
    port: 80
    nodePort: 30080
  ingress:
    enabled: false

# 데이터 옵저버 설정
data-observer:
  enabled: true
  image:
    repository: ai-sw-ide/data-observer
    tag: "latest"
  nfs:
    enabled: true
    server: "your-nfs-server.example.com"
    path: "/path/to/nfs/share"

# PostgreSQL 설정
postgresql:
  enabled: true
  auth:
    database: "ai-sw-ide"
    username: "<DB_USER>"
    password: "<DB_PASSWORD>"
```

### NFS 설정

Data Observer에서 NFS 볼륨을 사용하려면:

```yaml
data-observer:
  nfs:
    enabled: true
    server: "<YOUR_NFS_SERVER_IP>"  # NFS 서버 IP
    path: "/mnt/nfs/data"    # NFS 공유 경로
    mountPath: "/nfsvolume"  # 컨테이너 내 마운트 경로
```

### NodePort 접근

Frontend와 Backend는 NodePort 서비스로 구성되어 있어 클러스터 외부에서 직접 접근 가능합니다:

```bash
# 노드 IP 확인
export NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 서비스 접근
echo "Frontend: http://$NODE_IP:30080"
echo "Backend API: http://$NODE_IP:30800/docs"
```

### Ingress 설정 (선택사항)

필요시 Ingress를 활성화할 수 있습니다:

```yaml
frontend:
  ingress:
    enabled: true
    className: "nginx"
    annotations:
      nginx.ingress.kubernetes.io/rewrite-target: /
    hosts:
      - host: ai-sw-ide.yourdomain.com
        paths:
          - path: /
            pathType: Prefix
```

## 업그레이드

```bash
helm upgrade ai-sw-ide . -n ai-sw-ide
```

## 제거

```bash
helm uninstall ai-sw-ide -n ai-sw-ide
```

## 문제 해결

### 1. Pod 상태 확인
```bash
kubectl get pods -n ai-sw-ide
```

### 2. 로그 확인
```bash
kubectl logs -n ai-sw-ide deployment/ai-sw-ide-backend
kubectl logs -n ai-sw-ide deployment/ai-sw-ide-frontend  
kubectl logs -n ai-sw-ide deployment/ai-sw-ide-data-observer
```

### 3. 서비스 확인
```bash
kubectl get svc -n ai-sw-ide
```

### 4. Ingress 확인
```bash
kubectl get ingress -n ai-sw-ide
```

## 개발

### 서비스 접근 방법

#### NodePort로 직접 접근 (권장)
```bash
# 노드 IP 확인
export NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")

# 서비스 접근
echo "Frontend: http://$NODE_IP:30080"
echo "Backend API: http://$NODE_IP:30800/docs"
```

#### 포트 포워딩으로 접근
```bash
# Backend API
kubectl port-forward -n ai-sw-ide svc/ai-sw-ide-backend 8000:8000

# Frontend
kubectl port-forward -n ai-sw-ide svc/ai-sw-ide-frontend 8080:80

# Data Observer  
kubectl port-forward -n ai-sw-ide svc/ai-sw-ide-data-observer 8001:8000

# PostgreSQL
kubectl port-forward -n ai-sw-ide svc/ai-sw-ide-postgresql 5432:5432
```

## 폴더 구조

```
helm-chart/
├── Chart.yaml              # 차트 메타데이터
├── values.yaml             # 기본 설정값
├── templates/              # 메인 템플릿
│   ├── _helpers.tpl        # 헬퍼 함수
│   └── NOTES.txt          # 설치 후 안내사항
├── charts/                 # Subchart들
│   ├── backend/           # Backend subchart
│   ├── frontend/          # Frontend subchart
│   └── data-observer/     # Data Observer subchart
├── README.md              # 이 파일
├── install-guide.md       # 상세 설치 가이드
└── quick-start.sh         # 빠른 설치 스크립트
```

## 라이선스

이 프로젝트는 Apache2.0 라이선스를 따릅니다.
