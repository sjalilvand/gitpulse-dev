3. `docs/architecture.md` (English architecture)

```markdown
# GitPulse AI Architecture

## Overview

GitPulse AI follows an **event-driven microservices architecture** using Apache Kafka as the central message broker. The system ingests GitHub data via API polling or webhooks, processes it through dedicated workers, and stores it in both PostgreSQL (operational) and ClickHouse (analytics). A React frontend and Grafana provide visualization and AI-powered insights.

## High-Level Diagram
GitHub API / Webhook
│
▼
FastAPI Backend
│
▼
Kafka Broker
│
├─── Commit Worker ─────> PostgreSQL
├─── PR Worker ──────────> PostgreSQL
├─── Issue Worker ───────> PostgreSQL
├─── Analytics Worker ───> ClickHouse
├─── AI Worker ──────────> PostgreSQL (reports)
│
▼
React Frontend Grafana

text

## Component Details

### 1. Backend API (FastAPI)
- Manages repositories (CRUD).
- Triggers manual sync operations.
- Handles GitHub webhook events (optional).
- Provides REST endpoints for frontend consumption.
- Publishes events to Kafka topics.

### 2. Apache Kafka
- **Topics**:
  - `github.commits.created`
  - `github.pull_requests.created`
  - `github.issues.created`
- **Configuration**: KRaft mode (no Zookeeper required).
- **Auto-create topics** enabled for development.

### 3. Workers (Python Consumers)
- **Commit Worker**: Consumes commit events, saves to PostgreSQL.
- **PR Worker**: Saves pull requests, initial risk scoring.
- **Issue Worker**: Saves issues, prepares for classification.
- **Analytics Worker**: Aggregates data into ClickHouse tables.
- **AI Worker**: Generates summaries, risk analyses, release notes using AvalAI.

All workers are independent and can be scaled separately.

### 4. Databases
- **PostgreSQL**: Primary operational store. Tables: `repositories`, `commits`, `pull_requests`, `issues`, `commit_analytics`, `issue_analytics`, `ai_reports`.
- **ClickHouse**: High-performance analytical store. Tables: `commit_events`, `issue_events`. Optimized for time-series aggregation.

### 5. Frontend (React)
- Built with Vite, TypeScript, TailwindCSS, Recharts.
- Pages: Dashboard, Repository List, Repository Detail (tabs: Commits, PRs, Issues, AI Reports).
- AI Reports tab includes Weekly Summary, PR Risk Analysis, and Release Notes Generator.
- Settings page for scheduler control.

### 6. Grafana
- Connected to PostgreSQL for analytics dashboards.
- Panels: Commit activity over time, Top contributors, Issue status distribution.
- (Optional) Can connect to ClickHouse for larger datasets.

### 7. Background Scheduler
- APScheduler inside the backend periodically (every 5 minutes) fetches new commits, PRs, and issues from GitHub for all tracked repositories.
- Can be toggled on/off via API and UI.

## Data Flow

1. User adds a GitHub repository via frontend → backend stores metadata.
2. On manual sync or scheduler trigger, backend fetches recent commits/PRs/issues via PyGithub.
3. Each item is wrapped as an event and published to the appropriate Kafka topic.
4. Workers consume events and persist them to PostgreSQL and ClickHouse.
5. Analytics worker pushes aggregated data to ClickHouse for Grafana.
6. AI worker (or on-demand API) queries OpenAI-compatible API for summaries, risk analysis, etc.
7. Frontend queries backend REST APIs to display data.

## Deployment

- Docker Compose orchestrates all services.
- `docker-compose.yml` defines PostgreSQL, ClickHouse, Kafka, Backend, Frontend, Grafana, and worker containers.
- Environment variables managed via `.env` file.