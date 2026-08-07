from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RepositoryBase(BaseModel):
    url: str

class RepositoryCreate(RepositoryBase):
    pass

class RepositoryResponse(RepositoryBase):
    id: int
    github_id: int
    name: str
    full_name: str
    owner: str
    description: Optional[str] = None
    default_branch: str
    language: Optional[str] = None
    stars: int
    forks: int
    open_issues_count: int
    last_synced_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True