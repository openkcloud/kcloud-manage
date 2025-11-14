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
- **Tech Stack**: FastAPI, Python, PostgreSQL, SQLAlchemy
- **Features**: Server Management, GPU Resource Management, Storage Management, etc
- **Documentation**: [Backend README](AI_SW_IDE/backend/README.md)

### Frontend (`AI_SW_IDE/frontend/`)
- **Tech Stack**: React, Vite, TailwindCSS
- **Features**: Web dashboard UI, GPU Server Creation, Real-time Monitoring, Storage Management, etc
- **Documentation**: [Frontend README](AI_SW_IDE/frontend/README.md)

### Data Observer (`AI_SW_IDE/data_observer/`)
- **Tech Stack**: FastAPI, Python
- **Features**: NFS Volume Directory Browsing 

### Helm Chart (`AI_SW_IDE/helm-chart/`)
- Subchart-based architecture (Backend, Frontend, Data Observer)
- Automatic Bitnami PostgreSQL installation

  
