from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.db.models.pull_request import PullRequest

router = APIRouter(prefix="/api/v1/pull-requests", tags=["pull_requests"])

@router.get("/")
def list_prs(repo_id: int = None, db: Session = Depends(get_db)):
    query = db.query(PullRequest)
    if repo_id:
        query = query.filter(PullRequest.repo_id == repo_id)
    return query.order_by(PullRequest.created_at.desc()).limit(50).all()