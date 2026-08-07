from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.db.postgres import Base
from datetime import datetime

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, nullable=False)
    github_pr_id = Column(Integer, unique=True)  # GitHub PR number within repo? Actually PR ID is unique globally
    number = Column(Integer)  # PR number in repo
    title = Column(String)
    body = Column(String, nullable=True)
    state = Column(String)  # open, closed, merged
    author_username = Column(String)
    base_branch = Column(String)
    head_branch = Column(String)
    merged = Column(Boolean, default=False)
    merged_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    changed_files = Column(Integer, default=0)
    risk_score = Column(Integer, default=0)  # بعداً AI پر می‌کند
    ai_summary = Column(String, nullable=True)