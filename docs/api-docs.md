markdown
# GitPulse AI API Documentation

Base URL: `http://localhost:8001/api/v1`

## Endpoints

### Repositories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/repositories/` | List all repositories |
| POST | `/repositories/` | Add a new repository (body: `{"url": "..."}`) |
| GET | `/repositories/{id}` | Get single repository |
| POST | `/repositories/{id}/sync` | Sync commits for a repository |
| POST | `/repositories/{id}/sync-pr` | Sync pull requests |
| POST | `/repositories/{id}/sync-issues` | Sync issues |

### Commits

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/commits/?repo_id=1` | List commits (optional filter by repo_id) |

### Pull Requests

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pull-requests/?repo_id=1` | List pull requests |

### Issues

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/issues/?repo_id=1` | List issues |

### AI Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ai/repositories/{id}/weekly-summary` | Generate weekly summary |
| POST | `/ai/repositories/{id}/release-notes` | Generate release notes |
| POST | `/ai/pull-requests/{id}/risk-analysis` | Analyze PR risk |
| POST | `/ai/issues/{id}/classify` | Classify an issue |

### Scheduler

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/scheduler/status` | Get scheduler status |
| POST | `/scheduler/trigger-sync` | Trigger immediate sync |
| POST | `/scheduler/toggle-auto-sync` | Toggle automatic sync on/off |

### Webhook

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhooks/github` | GitHub webhook receiver (requires signature verification) |

## Example Requests

### Add a repository
```bash
curl -X POST http://localhost:8001/api/v1/repositories/ \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com/fastapi/fastapi"}'
Generate weekly summary
bash
curl -X POST http://localhost:8001/api/v1/ai/repositories/1/weekly-summary
Trigger manual sync
bash
curl -X POST http://localhost:8001/api/v1/scheduler/trigger-sync