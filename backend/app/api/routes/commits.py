from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.db.models.commit import Commit

router = APIRouter(prefix="/api/v1/commits", tags=["commits"])

@router.get("/")
def list_commits(repo_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Commit)
    if repo_id:
        query = query.filter(Commit.repo_id == repo_id)
    return query.order_by(Commit.committed_at.desc()).limit(50).all()