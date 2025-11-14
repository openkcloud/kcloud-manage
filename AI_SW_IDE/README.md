# kcloud-manage
# AI_SW_IDE

GPU 리소스 모니터링 및 관리를 위한 대시보드 애플리케이션입니다.

## 프로젝트 구조

```
AI_SW_IDE/
├── backend/           # FastAPI 백엔드 서버
├── frontend/          # React 프론트엔드 애플리케이션
├── data_observer/     # NFS 데이터 모니터링 서비스
├── helm-chart/        # Kubernetes 배포용 Helm 차트
└── deploy.sh          # 기존 배포 스크립트
```

## 구성 요소

### Backend (`backend/`)
- **기술 스택**: FastAPI, Python
- **기능**: GPU 리소스 모니터링 API, 데이터베이스 연동
- **포트**: 8000

### Frontend (`frontend/`)
- **기술 스택**: React, Vite, TailwindCSS
- **기능**: 웹 기반 대시보드 UI
- **포트**: 80 (Nginx)

### Data Observer (`data_observer/`)
- **기술 스택**: FastAPI, Python
- **기능**: NFS 볼륨 데이터 모니터링 및 파일 시스템 분석
- **포트**: 8000

## Kubernetes 배포

### Helm Chart 사용 (권장)

Kubernetes 클러스터에 배포하려면 `helm-chart/` 폴더를 사용하세요:

```bash
cd helm-chart
./quick-start.sh
```

자세한 내용은 [helm-chart/README.md](helm-chart/README.md)를 참조하세요.

### 주요 특징
- **Subchart 구조**: Backend, Frontend, Data Observer가 각각 독립적인 subchart
- **PostgreSQL 통합**: Bitnami PostgreSQL 차트 자동 설치
- **NFS 볼륨 지원**: Data Observer용 NFS 자동 마운트
- **Ingress 지원**: 외부 접근을 위한 Ingress 설정
- **중앙 집중식 설정**: 최상단 values.yaml에서 모든 설정 관리

## 로컬 개발

### Backend 개발
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend 개발
```bash
cd frontend
npm install
npm run dev
```

### Data Observer 개발
```bash
cd data_observer
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API 문서

각 서비스는 FastAPI의 자동 생성 문서를 제공합니다:

- Backend API: `http://localhost:8000/docs`
- Data Observer API: `http://localhost:8001/docs`

## 환경 설정

각 컴포넌트는 환경 변수를 통해 설정됩니다:

### Backend
- `DATABASE_URL`: PostgreSQL 연결 URL
- `REDIS_URL`: Redis 연결 URL (선택사항)

### Frontend
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_DATA_OBSERVER_URL`: Data Observer URL

### Data Observer
- `NFS_ROOT`: NFS 마운트 경로 (기본: `/home/jovyan`)

## 라이선스

Apache 2.0