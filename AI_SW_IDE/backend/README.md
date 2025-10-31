# GPU Dashboard Backend

GPU 클러스터 관리를 위한 FastAPI 기반 백엔드 서비스입니다. Kubernetes 환경에서 GPU 리소스를 할당하고 관리하며, Jupyter Lab 서버를 동적으로 생성/삭제할 수 있는 기능을 제공합니다.

## 🚀 주요 기능

- **서버 관리**: Kubernetes Pod 기반 Jupyter Lab 서버 생성/삭제
- **GPU 리소스 관리**: MIG(Multi-Instance GPU) 및 전체 GPU 할당
- **스토리지 관리**: PVC(PersistentVolumeClaim) 및 NFS 마운트 지원
- **사용자 인증**: JWT 기반 사용자 인증 및 권한 관리
- **메트릭 수집**: GPU 및 노드 리소스 모니터링
- **프록시 서버**: Jupyter Lab 서버 접근을 위한 내부 프록시
- **파일 브라우징**: 외부 data-observer 서비스와 연동

## 📁 프로젝트 구조

```
backend/
├── app/
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   ├── test.py                 # 테스트 파일
│   ├── api/                    # API 라우터 및 엔드포인트
│   │   ├── router.py           # 메인 라우터 설정
│   │   └── routes/            
│   │       ├── auth.py         # 사용자 인증 관련 API
│   │       ├── server.py       # 서버(Pod) 관리 API
│   │       ├── storage.py      # 스토리지(PVC) 관리 API
│   │       ├── proxy.py        # Jupyter Lab 프록시 API
│   │       └── metrics.py      # 메트릭 수집 API
│   ├── core/                   # 핵심 설정
│   │   └── config.py           # 환경 설정 및 Kubernetes 클라이언트
│   ├── db/                     # 데이터베이스 관련
│   │   ├── session.py          # SQLAlchemy 세션 설정
│   │   ├── dependencies.py     # DB 의존성 주입
│   │   └── init_database.py    # 초기 데이터 로딩
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── user.py             # 사용자 모델
│   │   ├── gpu.py              # GPU 및 Flavor 모델
│   │   └── k8s.py              # Kubernetes 리소스 모델
│   ├── schemas/                # Pydantic 스키마
│   │   ├── k8s.py              # Kubernetes 관련 스키마
│   │   └── login.py            # 인증 관련 스키마
│   └── utils/                  # 유틸리티 함수
│       └── __init__.py         # 공통 유틸리티 함수
├── requirements.txt            # Python 의존성
├── local.env                   # 로컬 환경 변수
├── prod.env                    # 프로덕션 환경 변수
├── create_test_mapping.py      # 테스트 데이터 생성 스크립트
└── Dockerfile                  # Docker 이미지 빌드 파일
```

## 🛠️ 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Container Orchestration**: Kubernetes Python Client
- **Password Hashing**: Passlib
- **Environment Management**: python-dotenv
- **Real-time Communication**: WebSockets

## 📋 주요 API 엔드포인트

### 🔐 인증 (`/auth`)
- `POST /auth/login` - 사용자 로그인
- `POST /auth/refresh` - 토큰 갱신

### 🖥️ 서버 관리 (`/server`)
- `GET /server/list` - 전체 서버 목록 조회
- `GET /server/my-server` - 내 서버 목록 조회
- `GET /server/my-pvcs` - 내 PVC 목록 조회
- `POST /server/create-pod` - 새 서버(Pod) 생성
- `DELETE /server/delete-server` - 서버 삭제
- `GET /server/browse` - 파일 브라우징 (data-observer 연동)

### 💾 스토리지 관리 (`/storage`)
- `GET /storage/storage-list` - 내 스토리지 목록 조회
- `POST /storage/create-nfs-storage` - NFS 기반 PV/PVC 생성
- `DELETE /storage/storage` - 스토리지 삭제

### 📊 메트릭 (`/metrics`)
- `GET /metrics/gpu-metrics` - GPU 사용률 조회
- `GET /metrics/node-metrics` - 노드 리소스 조회

### 🔗 프록시 (`/proxy`)
- `GET /proxy/{server_id}/` - Jupyter Lab 프록시 접근
- WebSocket 및 정적 파일 프록시 지원

## 🔧 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`local.env` 또는 `prod.env` 파일을 참조하여 환경 변수를 설정합니다:
- `DATABASE_URL`: PostgreSQL 연결 URL
- `SECRET_KEY`: JWT 서명용 비밀키
- `NAMESPACE`: Kubernetes 네임스페이스
- 기타 Kubernetes 및 서비스 설정

### 3. 데이터베이스 초기화
```bash
python create_test_mapping.py  # 테스트 데이터 생성 (선택사항)
```

### 4. 애플리케이션 실행
```bash
# 개발 모드
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🐳 Docker 실행

```bash
# Docker 이미지 빌드
docker build -t ai-sw-ide-backend .

# 컨테이너 실행
docker run -p 8000:8000 --env-file prod.env ai-sw-ide-backend
```

## 🎯 주요 특징

### GPU 리소스 관리
- **MIG 지원**: A100 GPU의 Multi-Instance GPU 기능 활용
- **동적 할당**: 사용자 요청에 따른 GPU 리소스 실시간 할당
- **리소스 추적**: GPU 사용률 및 가용성 모니터링

### Kubernetes 통합
- **네이티브 지원**: Kubernetes Python Client를 통한 직접 제어
- **자동 정리**: 실패한 리소스 자동 정리 및 롤백
- **네임스페이스 격리**: 멀티 테넌트 환경 지원

### 스토리지 유연성
- **PVC 관리**: 동적 PersistentVolumeClaim 생성/삭제
- **NFS 지원**: 외부 NFS 서버 마운트 기능
- **사용자별 격리**: 사용자별 스토리지 리소스 분리

### 보안
- **JWT 인증**: 토큰 기반 stateless 인증
- **사용자 권한**: 리소스별 소유권 검증
- **CORS 지원**: 프론트엔드 연동을 위한 CORS 설정

## 🔗 연관 서비스

- **Frontend**: React 기반 웹 대시보드
- **Data Observer**: 파일 시스템 브라우징 서비스
- **Jupyter Hub**: 사용자 개발 환경 제공

## 📝 API 문서

애플리케이션 실행 후 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://<NODE-IP>:<NODEPORT>/docs`
- ReDoc: `http://<NODE-IP>:<NODEPORT>/redoc`

## 🤝 기여

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing-feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 [Apache 2.0 라이선스](LICENSE) 하에 배포됩니다. 