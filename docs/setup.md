# GitPulse AI Setup Guide

## Prerequisites

- **Docker** and **Docker Compose** (v2+)
- **Git**
- A **GitHub Personal Access Token** (classic) with `public_repo` scope (or `repo` for private repos).
- An **AvalAI API key** (or any OpenAI-compatible endpoint) – optional but recommended for AI features.

## Step-by-Step Installation

### 1. Clone the repository
```bash
git clone https://github.com/sjalilvand/gitpulse-dev.git
cd gitpulse-ai
2. Configure environment variables
bash
cp .env.example .env
Edit the .env file and set the following variables:

GITHUB_TOKEN: Your GitHub personal access token.

AVALAI_API_KEY: Your AvalAI API key (if using AI features).

AVALAI_BASE_URL: https://api.avalai.ir/v1 (or your custom endpoint).

GITHUB_WEBHOOK_SECRET: A random secret string (if using webhooks).

(Other variables already have sensible defaults.)

3. Start all services
bash
docker compose up -d
Wait a minute for all containers to become healthy. Check status with:

bash
docker compose ps
4. Access the application
Frontend: http://localhost:5173

Backend API: http://localhost:8001/health

Grafana: http://localhost:3000 (login: admin/admin)

ClickHouse Playground: http://localhost:8123/play

Adding Your First Repository
Open the frontend → click on مخازن (Repositories).

Enter a GitHub repository URL (e.g., https://github.com/fastapi/fastapi).

The repository will be added and its metadata displayed.

To sync commits/PRs/issues, either:

Go to the repository detail page and use the "Sync" buttons (manual), or

Wait for the automatic scheduler (every 5 minutes) to sync, or

Use the Settings page to trigger a manual full sync.

Enabling AI Features
Make sure your .env contains a valid AVALAI_API_KEY. The AI features (weekly summary, PR risk analysis, release notes) will be available in the AI Reports tab of each repository.

Setting Up Grafana Dashboards
Log into Grafana at http://localhost:3000.

Navigate to Data Sources → Add PostgreSQL.

Host: postgres:5432

Database: gitpulse

User: gitpulse

Password: gitpulse123

SSL: disable

Create a new dashboard with panels using queries from commit_analytics and issue_analytics tables.

Troubleshooting
Cannot connect to Docker Hub: Set a proxy in Docker Desktop settings or use a local registry mirror.

Backend not starting: Check logs with docker logs gitpulse-backend. Ensure GitHub token is valid.

Worker errors: Check individual worker logs (docker logs gitpulse-commit-worker, etc.).

Port conflicts: Change exposed ports in docker-compose.yml.

Stopping the Project
bash
docker compose down
(Add -v to remove volumes – caution, data will be lost.)

Development
Backend code is mounted as a volume; changes auto-reload.

Frontend uses Vite HMR; refresh the browser.

To rebuild after adding new Python dependencies, run docker compose up -d --build backend.