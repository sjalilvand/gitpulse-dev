from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.postgres import Base
from datetime import datetime

class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, nullable=False)  # ForeignKey موقتاً حذف شد
    commit_hash = Column(String, unique=True, index=True)
    author_name = Column(String)
    author_email = Column(String)
    author_username = Column(String)
    message = Column(String)
    branch = Column(String, default="main")
    commit_url = Column(String)
    committed_at = Column(DateTime)
    additions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    files_changed = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)