# kcloud-manage

Kubernetes monitoring platform for GPU resources.

## Project Structure

```
kcloud-manage/
├── AI_SW_IDE/          # AI Software IDE - GPU resource monitoring dashboard
│   ├── backend/        # FastAPI backend server
│   ├── frontend/       # React frontend application
│   ├── data_observer/  # NFS data monitoring service
│   ├── helm-chart/     # Helm chart for Kubernetes deployment
│   └── deploy.sh       # Legacy deployment script
└── LICENSE             # Apache 2.0 License
```

## Components

### Backend (`AI_SW_IDE/backend/`)
- **Tech Stack**: FastAPI, Python
- **Features**: GPU monitoring API, Kubernetes pod management, authentication, PostgreSQL integration, Prometheus metrics

### Frontend (`AI_SW_IDE/frontend/`)
- **Tech Stack**: React, Vite, TailwindCSS
- **Features**: Web dashboard UI, GPU node monitoring, pod management, storage management

### Data Observer (`AI_SW_IDE/data_observer/`)
- **Tech Stack**: FastAPI, Python
- **Features**: NFS volume monitoring, filesystem analysis

### Helm Chart (`AI_SW_IDE/helm-chart/`)
- Subchart-based architecture (Backend, Frontend, Data Observer)
- Automatic Bitnami PostgreSQL installation
- Centralized configuration via top-level values.yaml

  
## Prerequisites

- Kubernetes cluster (1.20+)
- Helm 3.x
- DCGM Exporter
- Prometheus
- NFS server (optional)

## Quick Start

### Kubernetes Deployment (Recommended)

```bash
cd AI_SW_IDE/helm-chart
./quick-start.sh
```

For details, see [AI_SW_IDE/helm-chart/README.md](AI_SW_IDE/helm-chart/README.md).

### Legacy Deployment

```bash
cd AI_SW_IDE
./deploy.sh
```

