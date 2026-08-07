from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.postgres import get_db
from app.db.models.repository import Repository
from app.schemas.repository import RepositoryCreate, RepositoryResponse
from app.services.github_service import fetch_repo_info, get_github_client, fetch_pull_requests, fetch_issues
from app.services.kafka_service import send_event



router = APIRouter(prefix="/api/v1/repositories", tags=["repositories"])

@router.get("/", response_model=List[RepositoryResponse])
def list_repositories(db: Session = Depends(get_db)):
    return db.query(Repository).all()

@router.post("/", response_model=RepositoryResponse, status_code=201)
def create_repository(repo_data: RepositoryCreate, db: Session = Depends(get_db)):
    try:
        info = fetch_repo_info(repo_data.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    existing = db.query(Repository).filter(Repository.github_id == info["github_id"]).first()
    if existing:
        raise HTTPException(status_code=409, detail="Repository already exists")

    db_repo = Repository(**info)
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo

@router.post("/{repo_id}/sync")
def sync_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    try:
        client = get_github_client()
        gh_repo = client.get_repo(repo.full_name)
        commits = gh_repo.get_commits()[:30]  # ۳۰ کامیت آخر

        for commit in commits:
            event = {
                "repo_id": repo.id,
                "repo_full_name": repo.full_name,
                "commit_hash": commit.sha,
                "author_name": commit.commit.author.name,
                "author_email": commit.commit.author.email,
                "author_username": commit.author.login if commit.author else "",
                "message": commit.commit.message,
                "branch": repo.default_branch,
                "additions": commit.stats.additions if commit.stats else 0,
                "deletions": commit.stats.deletions if commit.stats else 0,
                "files_changed": commit.stats.total if commit.stats else 0,
                "committed_at": commit.commit.author.date.isoformat()
            }
            send_event("github.commits.created", key=commit.sha, value=event)

        return {"message": f"Sent {len(list(commits))} commit events to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{repo_id}/sync-pr")
def sync_pull_requests(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    try:
        prs = fetch_pull_requests(repo.full_name, count=20)
        for pr in prs:
            event = {
                "repo_id": repo.id,
                "repo_full_name": repo.full_name,
                **pr
            }
            send_event("github.pull_requests.created", key=str(pr["github_pr_id"]), value=event)
        return {"message": f"Sent {len(prs)} pull request events to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{repo_id}/sync-issues")
def sync_issues(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    try:
        issues = fetch_issues(repo.full_name, count=20)
        for issue in issues:
            event = {
                "repo_id": repo.id,
                "repo_full_name": repo.full_name,
                **issue
            }
            send_event("github.issues.created", key=str(issue["github_issue_id"]), value=event)
        return {"message": f"Sent {len(issues)} issue events to Kafka"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{repo_id}", response_model=RepositoryResponse)
def get_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo