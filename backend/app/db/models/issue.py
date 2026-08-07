from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from app.db.postgres import Base
from datetime import datetime



class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, nullable=False)
    github_issue_id = Column(BigInteger, unique=True)
    number = Column(Integer)
    title = Column(String)
    body = Column(String, nullable=True)
    state = Column(String)  # open / closed
    author_username = Column(String)
    labels = Column(String, nullable=True)  # comma-separated
    category = Column(String, nullable=True)  # later filled by AI
    priority = Column(String, nullable=True)
    ai_summary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)