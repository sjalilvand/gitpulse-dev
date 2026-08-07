from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.postgres import engine, Base
from app.db.models.commit import Commit  # اضافه کن
from app.api.routes import repositories
from app.api.routes import repositories, commits
from app.api.routes import pull_requests
from app.api.routes import issues
from app.db.models.analytics import CommitAnalytics, IssueAnalytics
from app.api.routes import ai_reports
from app.api.routes import webhooks
from app.api.routes import scheduler_control






@asynccontextmanager
async def lifespan(app: FastAPI):
    # ایجاد جداول در صورت عدم وجود
    Base.metadata.create_all(bind=engine)
    import threading
    from app.workers.commit_worker import start_worker as start_commit_worker
    from app.workers.pr_worker import start_pr_worker
    from app.workers.issue_worker import start_issue_worker
    from app.workers.analytics_worker import start_analytics_worker
    threading.Thread(target=start_commit_worker, daemon=True).start()
    threading.Thread(target=start_pr_worker, daemon=True).start()
    threading.Thread(target=start_issue_worker, daemon=True).start()
    threading.Thread(target=start_analytics_worker, daemon=True).start()
    # راه‌اندازی scheduler
    from app.services.scheduler import start_scheduler
    start_scheduler()
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

# Router ها
app.include_router(repositories.router)
app.include_router(commits.router)
app.include_router(pull_requests.router)
app.include_router(issues.router)
app.include_router(ai_reports.router)
app.include_router(webhooks.router)
app.include_router(scheduler_control.router)





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