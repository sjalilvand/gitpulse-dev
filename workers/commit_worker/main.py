from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.postgres import engine, Base
from app.db.models.repository import Repository
from app.db.models.commit import Commit
from app.api.routes import repositories
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ایجاد جداول
    Base.metadata.create_all(bind=engine)
    # راه‌اندازی worker در ترد جدا
    from app.workers.commit_worker import start_worker
    worker_thread = threading.Thread(target=start_worker, daemon=True)
    worker_thread.start()
    yield

app = FastAPI(
    title="GitPulse AI",
    description="AI-Powered GitHub Analytics & Monitoring Platform",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(repositories.router)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0",
        "services": {
            "api": "running"
        }
    }

@app.get("/api/v1/status")
async def get_status():
    return {
        "status": "operational",
        "environment": "development",
        "timestamp": "2026-08-07T00:00:00Z"
    }