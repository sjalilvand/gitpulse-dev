from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.postgres import get_db
from app.db.models.repository import Repository
from app.db.models.commit import Commit
from app.services.ai_service import generate_weekly_summary, analyze_pr_risk, classify_issue

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])


@router.post("/repositories/{repo_id}/weekly-summary")
def get_weekly_summary(repo_id: int, db: Session = Depends(get_db)):
    repo = db.query(Repository).filter(Repository.id == repo_id).first()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    commits = db.query(Commit).filter(Commit.repo_id == repo_id) \
        .order_by(Commit.committed_at.desc()).limit(30).all()

    commit_data = [{
        "message": c.message,
        "author": c.author_username,
        "hash": c.commit_hash
    } for c in commits]

    summary = generate_weekly_summary(repo.full_name, commit_data)
    return {"repo_id": repo_id, "summary": summary}


@router.post("/pull-requests/{pr_id}/risk-analysis")
def get_pr_risk_analysis(pr_id: int, db: Session = Depends(get_db)):
    from app.db.models.pull_request import PullRequest
    pr = db.query(PullRequest).filter(PullRequest.id == pr_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="PR not found")

    pr_data = {
        "title": pr.title,
        "additions": pr.additions,
        "deletions": pr.deletions,
        "changed_files": pr.changed_files,
        "base_branch": pr.base_branch
    }

    analysis = analyze_pr_risk(pr_data)
    return {"pr_id": pr_id, **analysis}


@router.post("/issues/{issue_id}/classify")
def classify_issue_endpoint(issue_id: int, db: Session = Depends(get_db)):
    from app.db.models.issue import Issue
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    classification = classify_issue(issue.title, issue.body or "")
    return {"issue_id": issue_id, **classification}