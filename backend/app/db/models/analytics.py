from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.postgres import Base

class CommitAnalytics(Base):
    __tablename__ = "commit_analytics"
    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    repo_full_name = Column(String)
    commit_hash = Column(String, unique=True)
    author_username = Column(String)
    branch = Column(String)
    message = Column(String)
    additions = Column(Integer)
    deletions = Column(Integer)
    files_changed = Column(Integer)
    committed_at = Column(DateTime)

class IssueAnalytics(Base):
    __tablename__ = "issue_analytics"
    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer)
    repo_full_name = Column(String)
    github_issue_id = Column(Integer, unique=True)
    number = Column(Integer)
    title = Column(String)
    state = Column(String)
    author_username = Column(String)
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    created_at = Column(DateTime)
    closed_at = Column(DateTime, nullable=True)