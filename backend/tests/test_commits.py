def test_list_commits(client, db_session):
    # مستقیماً یک کامیت در دیتابیس درج می‌کنیم و سپس API را تست می‌کنیم
    from app.db.models.commit import Commit
    from datetime import datetime
    db = db_session
    commit = Commit(
        repo_id=1,
        commit_hash="abc123",
        author_name="Test",
        author_email="test@test.com",
        author_username="test",
        message="Test commit",
        branch="main",
        commit_url="https://github.com/test/commit/abc123",
        committed_at=datetime.utcnow(),
        additions=10,
        deletions=2,
        files_changed=3
    )
    db.add(commit)
    db.commit()

    response = client.get("/api/v1/commits/?repo_id=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["commit_hash"] == "abc123"