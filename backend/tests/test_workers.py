import json
from unittest.mock import patch, MagicMock
from app.workers.commit_worker import process_commit
from app.db.models.commit import Commit

def test_process_commit(db_session):
    event = {
        "repo_id": 1,
        "repo_full_name": "user/test",
        "commit_hash": "def456",
        "author_name": "Test",
        "author_email": "test@test.com",
        "author_username": "tester",
        "message": "Worker test",
        "branch": "main",
        "additions": 5,
        "deletions": 1,
        "files_changed": 2,
        "committed_at": "2026-08-08T00:00:00"
    }
    process_commit(event)
    db = db_session
    commits = db.query(Commit).all()
    assert len(commits) == 1
    assert commits[0].commit_hash == "def456"