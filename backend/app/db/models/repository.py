from sqlalchemy import Column, Integer, String, DateTime
from app.db.postgres import Base
from datetime import datetime

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, index=True)
    full_name = Column(String, unique=True, index=True)
    owner = Column(String)
    url = Column(String)
    description = Column(String, nullable=True)
    default_branch = Column(String, default="main")
    language = Column(String, nullable=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)
    open_issues_count = Column(Integer, default=0)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)