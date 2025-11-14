# AI_SW_IDE Frontend

GPU 클러스터 관리를 위한 웹 대시보드의 프론트엔드 애플리케이션입니다. React와 Material Tailwind를 기반으로 구축되었으며, GPU 서버 생성, 모니터링, 스토리지 관리 등의 기능을 제공합니다.

## 🚀 주요 기능

- **GPU 서버 생성**: CPU, Memory, GPU 자원을 선택하여 서버 생성
- **실시간 모니터링**: GPU 클러스터 상태 및 실행 중인 Pod 모니터링
- **스토리지 관리**: PVC 기반 파일 시스템 탐색 및 관리
- **사용자 인증**: JWT 기반 로그인/로그아웃 시스템
- **반응형 UI**: 모든 디바이스에서 최적화된 사용자 경험

## 🛠 기술 스택

- **Frontend Framework**: React 19.0.0
- **Build Tool**: Vite 6.1.0
- **UI Library**: Material Tailwind 2.1.10
- **Styling**: Tailwind CSS 3.4.17
- **Icons**: Heroicons 2.2.0
- **Routing**: React Router DOM 7.4.0
- **Authentication**: JWT Decode 4.0.0

## 📁 프로젝트 구조

```
src/
├── components/          # 재사용 가능한 UI 컴포넌트
│   ├── Secure/         # 인증 관련 컴포넌트
│   ├── ExpendingRadioButton.jsx  # 서버 생성 폼
│   ├── RunningPodTable.jsx       # 실행 중인 Pod 테이블
│   ├── MyServerCard.jsx          # 서버 카드 컴포넌트
│   ├── Navbar.jsx               # 네비게이션 바
│   ├── Sidebar.jsx              # 사이드바
│   ├── SignIn.jsx               # 로그인 컴포넌트
│   ├── GPUComponent.jsx         # GPU 관련 컴포넌트
│   ├── GPUNode.jsx              # GPU 노드 표시
│   ├── Loading.jsx              # 로딩 스피너
│   └── ...
├── layout/             # 레이아웃 컴포넌트
│   ├── DashboardStatus.jsx      # 대시보드 메인 화면
│   ├── CreatePod.jsx            # 서버 생성 페이지
│   ├── MyServer.jsx             # 내 서버 관리
│   ├── StorageManagement.jsx    # 스토리지 관리
│   └── Sidebar.jsx              # 레이아웃용 사이드바
├── pages/              # 페이지 컴포넌트
│   ├── SignInPage.jsx           # 로그인 페이지
│   ├── AdminDashboard.jsx       # 관리자 대시보드
│   └── UserDashboard.jsx        # 사용자 대시보드
├── utils/              # 유틸리티 함수
│   ├── auth.js                  # 인증 관련 함수
│   └── mockAuth.jsx             # 모킹용 인증
├── context/            # React Context 설정
├── assets/             # 정적 자원
├── public/             # Public 파일
├── App.jsx             # 메인 앱 컴포넌트
├── main.jsx            # 엔트리 포인트
└── index.css           # 글로벌 CSS
```

## 🔧 설치 및 실행

### 필수 요구사항
- Node.js 18+ 
- npm 또는 yarn

### 설치
```bash
# 의존성 설치
npm install
```

### 개발 서버 실행
```bash
# 개발 모드로 실행 (포트 4000)
npm run dev
```
브라우저에서 `http://localhost:4000`으로 접속

### 빌드
```bash
# 프로덕션 빌드
npm run build
```

### 린트 검사
```bash
# ESLint 실행
npm run lint
```

## 🌐 환경 변수

`.env` 파일을 생성하여 다음 환경변수를 설정하세요:

```env
VITE_API_URL=http://localhost:8000  # 백엔드 API URL
```

## 📝 주요 컴포넌트 설명

### 1. 대시보드 (DashboardStatus)
- GPU 클러스터 전체 상태 모니터링
- 노드별 GPU, CPU, Memory 사용량 표시
- 실시간 업데이트 (15초 간격)

### 2. 서버 생성 (ExpendingRadioButton)
- 단계별 하드웨어 선택 (CPU → Memory → GPU)
- PVC 선택 (신규 생성 또는 기존 사용)
- 서버 이름 및 설명 입력

### 3. 스토리지 관리 (StorageManagement)
- PVC 목록 표시
- 파일 시스템 탐색
- 폴더/파일 정보 표시

### 4. 실행 중인 서버 테이블 (RunningPodTable)
- TAG 기반 서버 분류 (JUPYTER, LEGEND, DEV)
- 사용자, 자원 사용량, 생성일 표시
- 실시간 업데이트 (60초 간격)

## 🔐 인증 시스템

- JWT 기반 토큰 인증
- Access Token + Refresh Token 방식
- 자동 토큰 갱신
- 로그아웃 시 토큰 제거

## 🎨 UI/UX 특징

- **Material Design**: Material Tailwind 기반 일관된 디자인
- **반응형**: 다양한 화면 크기 지원
- **다크 모드**: 사용자 선호도에 따른 테마 지원
- **애니메이션**: Framer Motion을 활용한 부드러운 전환효과
- **접근성**: ARIA 라벨 및 키보드 네비게이션 지원

## 🔄 API 연동

백엔드 API와의 통신을 위한 주요 엔드포인트:

- `GET /server/list` - 실행 중인 서버 목록
- `POST /server/create-pod` - 새 서버 생성
- `GET /server/my-server` - 내 서버 목록
- `GET /server/my-pvcs` - PVC 목록
- `GET /server/browse` - 파일 시스템 탐색
- `GET /metrics/gpu-resource` - GPU 자원 모니터링
- `GET /metrics/node-resource` - 노드 자원 정보

## 🐳 Docker 배포

```bash
# Docker 이미지 빌드
docker build -t gpu-dashboard-frontend .

# 컨테이너 실행
docker run -p 80:80 gpu-dashboard-frontend
```

## 📄 라이센스

이 프로젝트는 MIT 라이센스 하에 있습니다.

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해 주세요.
