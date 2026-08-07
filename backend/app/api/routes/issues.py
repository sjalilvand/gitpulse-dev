from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.db.models.issue import Issue

router = APIRouter(prefix="/api/v1/issues", tags=["issues"])

@router.get("/")
def list_issues(repo_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Issue)
    if repo_id:
        query = query.filter(Issue.repo_id == repo_id)
    return query.order_by(Issue.created_at.desc()).limit(50).all()