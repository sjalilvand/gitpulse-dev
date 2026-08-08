from unittest.mock import patch

def test_weekly_summary(client, db_session):
    # یک مخزن و چند کامیت در دیتابیس ایجاد می‌کنیم
    from app.db.models.repository import Repository
    from app.db.models.commit import Commit
    from datetime import datetime
    db = db_session
    repo = Repository(github_id=1, name="test", full_name="user/test", owner="user", url="http://example.com")
    db.add(repo)
    db.commit()
    db.refresh(repo)

    commit = Commit(repo_id=repo.id, commit_hash="xyz", author_name="T", author_email="t@t.com",
                    author_username="t", message="initial commit", branch="main",
                    commit_url="http://x.com", committed_at=datetime.utcnow())
    db.add(commit)
    db.commit()

    mock_summary = "Summary in Persian"
    with patch("app.api.routes.ai_reports.generate_weekly_summary", return_value=mock_summary):
        response = client.post(f"/api/v1/ai/repositories/{repo.id}/weekly-summary")
    assert response.status_code == 200
    assert response.json()["summary"] == mock_summary