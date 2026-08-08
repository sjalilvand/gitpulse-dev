from unittest.mock import patch, MagicMock
from app.schemas.repository import RepositoryCreate

MOCK_REPO_INFO = {
    "github_id": 12345,
    "name": "test-repo",
    "full_name": "user/test-repo",
    "owner": "user",
    "url": "https://github.com/user/test-repo",
    "description": "A test repo",
    "default_branch": "main",
    "language": "Python",
    "stars": 10,
    "forks": 2,
    "open_issues_count": 3
}

def test_create_repository(client, db_session):
    with patch("app.api.routes.repositories.fetch_repo_info", return_value=MOCK_REPO_INFO):
        response = client.post("/api/v1/repositories/", json={"url": "https://github.com/user/test-repo"})
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "user/test-repo"
    assert data["github_id"] == 12345

def test_create_duplicate_repository(client, db_session):
    with patch("app.api.routes.repositories.fetch_repo_info", return_value=MOCK_REPO_INFO):
        client.post("/api/v1/repositories/", json={"url": "https://github.com/user/test-repo"})
        response = client.post("/api/v1/repositories/", json={"url": "https://github.com/user/test-repo"})
    assert response.status_code == 409

def test_list_repositories(client, db_session):
    with patch("app.api.routes.repositories.fetch_repo_info", return_value=MOCK_REPO_INFO):
        client.post("/api/v1/repositories/", json={"url": "https://github.com/user/test-repo"})
    response = client.get("/api/v1/repositories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_get_repository(client, db_session):
    with patch("app.api.routes.repositories.fetch_repo_info", return_value=MOCK_REPO_INFO):
        create_resp = client.post("/api/v1/repositories/", json={"url": "https://github.com/user/test-repo"})
    repo_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/repositories/{repo_id}")
    assert response.status_code == 200
    assert response.json()["full_name"] == "user/test-repo"

def test_sync_repository(client, db_session):
    # نیاز به mock کردن Kafka و GitHub
    with patch("app.api.routes.repositories.get_github_client") as mock_gh, \
         patch("app.api.routes.repositories.send_event") as mock_send:
        mock_repo = MagicMock()
        mock_repo.full_name = "user/test-repo"
        mock_repo.default_branch = "main"
        commit_mock = MagicMock()
        commit_mock.sha = "abc123"
        commit_mock.commit.author.name = "Test User"
        commit_mock.commit.author.email = "test@test.com"
        commit_mock.author.login = "testuser"
        commit_mock.commit.message = "Test commit"
        commit_mock.stats.additions = 10
        commit_mock.stats.deletions = 2
        commit_mock.stats.total = 5
        commit_mock.commit.author.date.isoformat.return_value = "2026-08-08T00:00:00"
        mock_repo.get_commits.return_value = [commit_mock]
        mock_gh.return_value.get_repo.return_value = mock_repo

        # ابتدا یک مخزن بسازیم
        with patch("app.api.routes.repositories.fetch_repo_info", return_value=MOCK_REPO_INFO):
            create_resp = client.post("/api/v1/repositories/", json={"url": "https://github.com/user/test-repo"})
        repo_id = create_resp.json()["id"]
        response = client.post(f"/api/v1/repositories/{repo_id}/sync")
    assert response.status_code == 200
    assert mock_send.call_count == 1