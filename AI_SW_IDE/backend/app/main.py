# app/main.py
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.db.session import engine, Base
from app.api.router import api_router
from app.api.routes.proxy import proxy_kernelspecs, proxy_static_files, proxy_nbextensions
import csv
from app.models import user, gpu, k8s
from app.db.session import SessionLocal
from app.core.config import CORS_ORIGINS, APP_PORT, GPU_FETCH
from app.db.init_database import init_users_from_csv, init_flavors_from_csv
from app.db.fetch_gpu import sync_flavors_to_db, sync_gpu_pod_status_from_prometheus
from app.core.logger import app_logger

async def scheduled_sync_gpu_flavors():
    """30초마다 실행되는 GPU 플레이버 동기화 작업"""
    try:
        await sync_flavors_to_db()  # gpu_flavor 테이블 동기화
        await sync_gpu_pod_status_from_prometheus()  # servers 테이블 동기화
    except Exception as e:
        app_logger.error(f"GPU sync error: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 개발 환경에서 테이블 자동 생성 (프로덕션에서는 Alembic 등으로 관리)
    Base.metadata.create_all(bind=engine)
    init_users_from_csv("./app/db/default_users.csv")
    init_flavors_from_csv("./app/db/default_gpu_flavors.csv")
    
    # APScheduler 시작
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        scheduled_sync_gpu_flavors, 
        "interval", 
        seconds=GPU_FETCH,
        id="sync_gpu_flavors",
        replace_existing=True
    )
    scheduler.start()
    app_logger.info(f"GPU sync scheduler started ({GPU_FETCH}s interval)")
    
    yield
    
    # 앱 종료 시 스케줄러 정리
    scheduler.shutdown()
    app_logger.info("GPU sync scheduler stopped")

app = FastAPI(lifespan=lifespan)

# 로깅 간섭을 피하기 위해 미들웨어 제거
# proxy 로그가 너무 많으면 uvicorn 시작 옵션으로 조정하세요:
# uvicorn app.main:app --log-level warning

# CORS 미들웨어 설정 (개발 단계에서는 "*" 사용, 프로덕션에서는 허용할 도메인 명시)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            *CORS_ORIGINS,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# kernelspecs 등의 static 파일을 위한 직접 라우터 등록
app.add_api_route("/kernelspecs/{path:path}", proxy_kernelspecs, methods=["GET"])
app.add_api_route("/static/{path:path}", proxy_static_files, methods=["GET"])
app.add_api_route("/nbextensions/{path:path}", proxy_nbextensions, methods=["GET"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API using OAuth2 Password Flow",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2Password": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/auth/login",
                    "scopes": {}
                }
            }
        }
    }
    # 각 endpoint에 보안 설정을 추가합니다.
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"OAuth2Password": []})
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application."}


