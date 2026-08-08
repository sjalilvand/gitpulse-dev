# GitPulse AI

**AI-Powered GitHub Analytics & Monitoring Platform**

GitPulse AI is a full-stack, event-driven platform that ingests GitHub repository data, processes it through Apache Kafka, stores it in PostgreSQL and ClickHouse, and exposes rich analytics via a React dashboard and Grafana. AI-powered features provide weekly summaries, PR risk analysis, issue classification, and automated release notes.

![GitPulse AI Dashboard](docs/screenshot.png) <!-- Optional: add a screenshot -->

## 🚀 Features

- **Real-time & Batch GitHub Sync** – Webhooks or scheduled polling keep data fresh.
- **Event-Driven with Kafka** – Commits, Pull Requests, and Issues flow through dedicated topics.
- **Multi-Database Storage** – PostgreSQL for operational data, ClickHouse for fast analytics.
- **AI Integration** – Weekly summaries, PR risk assessment, issue categorization, and release notes via AvalAI (or OpenAI-compatible API).
- **Modern Frontend** – React + TypeScript + TailwindCSS dashboard with charts (Recharts) and multi-tab views.
- **Grafana Dashboards** – Pre-configured dashboards for commit activity, contributor stats, and system health.
- **Background Scheduler** – Automatic periodic sync with manual trigger option.
- **CI/CD Ready** – GitHub Actions workflow for linting and testing.
- **Comprehensive Documentation** – Bilingual (English & Persian) architecture, setup, and API docs.

## 🏗️ Architecture

See the full [Architecture Document](docs/architecture.md).

## 🛠️ Tech Stack

| Layer          | Technology |
|----------------|------------|
| Backend        | Python, FastAPI, SQLAlchemy, Alembic |
| Frontend       | React, TypeScript, Vite, TailwindCSS, Recharts |
| Message Queue  | Apache Kafka (KRaft mode) |
| Databases      | PostgreSQL (operational), ClickHouse (analytics) |
| AI             | AvalAI (OpenAI compatible) or Ollama |
| Monitoring     | Grafana |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub, GitHub Actions |

## 📦 Quick Start

See the [Setup Guide](docs/setup.md) for detailed instructions.

```bash
git clone https://github.com/sjalilvand/gitpulse-dev.git
cd gitpulse-ai
cp .env.example .env   # Edit with your tokens
docker compose up -d
Frontend: http://localhost:5173

Backend API: http://localhost:8001 (health: /health)

Grafana: http://localhost:3000 (admin/admin)

ClickHouse Playground: http://localhost:8123/play

📚 Documentation
Setup Guide (English) / راهنمای نصب (Persian)

Architecture (English) / معماری (Persian)

API Reference (English) / مستندات API (Persian)

🧪 Testing
Run backend tests locally (requires Python 3.11):

bash
cd backend
pip install -r requirements.txt
pytest
The CI pipeline (.github/workflows/ci.yml) automatically runs tests on each push.

🤝 Contributing
Contributions are welcome! Please open an issue or pull request. See the roadmap for planned features (if available).

📜 License
MIT