# AI SOFTWARE IDE Backend

FastAPI-based backend service for GPU cluster management. Provides functionality to allocate and manage GPU resources in a Kubernetes environment and dynamically create/delete Jupyter Lab servers.

## 🚀 Key Features

- **Server Management**: Create/delete Kubernetes Pod-based Jupyter Lab servers
- **GPU Resource Management**: MIG (Multi-Instance GPU) and full GPU allocation
- **Storage Management**: PVC (PersistentVolumeClaim) and NFS mount support
- **User Authentication**: JWT-based user authentication and authorization
- **Metrics Collection**: GPU and node resource monitoring
- **Proxy Server**: Internal proxy for Jupyter Lab server access
- **File Browsing**: Integration with external data-observer service

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── test.py                 # Test file
│   ├── api/                    # API router and endpoints
│   │   ├── router.py           # Main router configuration
│   │   └── routes/            
│   │       ├── auth.py         # User authentication API
│   │       ├── server.py       # Server (Pod) management API
│   │       ├── storage.py      # Storage (PVC) management API
│   │       ├── proxy.py        # Jupyter Lab proxy API
│   │       └── metrics.py      # Metrics collection API
│   ├── core/                   # Core configuration
│   │   └── config.py           # Environment settings and Kubernetes client
│   ├── db/                     # Database related
│   │   ├── session.py          # SQLAlchemy session configuration
│   │   ├── dependencies.py     # DB dependency injection
│   │   └── init_database.py    # Initial data loading
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py             # User model
│   │   ├── gpu.py              # GPU and Flavor models
│   │   └── k8s.py              # Kubernetes resource models
│   ├── schemas/                # Pydantic schemas
│   │   ├── k8s.py              # Kubernetes related schemas
│   │   └── login.py            # Authentication related schemas
│   └── utils/                  # Utility functions
│       └── __init__.py         # Common utility functions
├── requirements.txt            # Python dependencies
├── local.env                   # Local environment variables
├── prod.env                    # Production environment variables
├── create_test_mapping.py      # Test data generation script
└── Dockerfile                  # Docker image build file
```

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Container Orchestration**: Kubernetes Python Client
- **Password Hashing**: Passlib
- **Environment Management**: python-dotenv
- **Real-time Communication**: WebSockets

## 📋 Main API Endpoints

### 🔐 Authentication (`/auth`)
- `POST /auth/login` - User login
- `POST /auth/refresh` - Token refresh

### 🖥️ Server Management (`/server`)
- `GET /server/list` - List all servers
- `GET /server/my-server` - List my servers
- `GET /server/my-pvcs` - List my PVCs
- `POST /server/create-pod` - Create new server (Pod)
- `DELETE /server/delete-server` - Delete server
- `GET /server/browse` - File browsing (data-observer integration)

### 💾 Storage Management (`/storage`)
- `GET /storage/storage-list` - List my storage
- `POST /storage/create-nfs-storage` - Create NFS-based PV/PVC
- `DELETE /storage/storage` - Delete storage

### 📊 Metrics (`/metrics`)
- `GET /metrics/gpu-metrics` - Get GPU usage
- `GET /metrics/node-metrics` - Get node resources

### 🔗 Proxy (`/proxy`)
- `GET /proxy/{server_id}/` - Jupyter Lab proxy access
- WebSocket and static file proxy support

## 🔧 Installation and Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Set environment variables by referring to `local.env` or `prod.env` files:
- `DATABASE_URL`: PostgreSQL connection URL
- `SECRET_KEY`: Secret key for JWT signing
- `NAMESPACE`: Kubernetes namespace
- Other Kubernetes and service settings

### 3. Initialize Database
```bash
python create_test_mapping.py  # Generate test data (optional)
```

### 4. Run Application
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🐳 Docker Execution

```bash
# Build Docker image
docker build -t ai-sw-ide-backend .

# Run container
docker run -p 8000:8000 --env-file prod.env ai-sw-ide-backend
```

## 🎯 Key Features

### GPU Resource Management
- **MIG Support**: Utilize Multi-Instance GPU functionality of A100 GPUs
- **Dynamic Allocation**: Real-time GPU resource allocation based on user requests
- **Resource Tracking**: Monitor GPU usage and availability

### Kubernetes Integration
- **Native Support**: Direct control via Kubernetes Python Client
- **Auto Cleanup**: Automatic cleanup and rollback of failed resources
- **Namespace Isolation**: Multi-tenant environment support

### Storage Flexibility
- **PVC Management**: Dynamic PersistentVolumeClaim creation/deletion
- **NFS Support**: External NFS server mount functionality
- **Per-User Isolation**: Separate storage resources per user

### Security
- **JWT Authentication**: Token-based stateless authentication
- **User Permissions**: Resource ownership verification
- **CORS Support**: CORS configuration for frontend integration

## 🔗 Related Services

- **Frontend**: React-based web dashboard
- **Data Observer**: File system browsing service
- **Jupyter Hub**: User development environment

## 📝 API Documentation

After running the application, you can check the auto-generated API documentation at:
- Swagger UI: `http://<NODE-IP>:<NODEPORT>/docs`
- ReDoc: `http://<NODE-IP>:<NODEPORT>/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing-feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is released under the [Apache 2.0 License](LICENSE). 