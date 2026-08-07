from clickhouse_driver import Client
from app.core.config import get_settings
from datetime import datetime

settings = get_settings()


def get_clickhouse_client():
    return Client(
        host='clickhouse',
        port=9000,
        user=settings.clickhouse_user,
        password=settings.clickhouse_password,
        database=settings.clickhouse_db
    )


def insert_commit_event(event: dict):
    client = get_clickhouse_client()
    # تبدیل committed_at از رشته به datetime
    committed_at = event['committed_at']
    if isinstance(committed_at, str):
        committed_at = datetime.fromisoformat(committed_at)

    client.execute(
        f"INSERT INTO {settings.clickhouse_db}.commit_events "
        "(event_id, repo_id, repo_full_name, commit_hash, author_username, branch, message, additions, deletions, files_changed, committed_at) "
        "VALUES",
        [(
            event.get('event_id', event.get('commit_hash')),
            event['repo_id'],
            event['repo_full_name'],
            event['commit_hash'],
            event['author_username'],
            event.get('branch', 'main'),
            event['message'],
            event.get('additions', 0),
            event.get('deletions', 0),
            event.get('files_changed', 0),
            committed_at
        )]
    )


def insert_issue_event(event: dict):
    client = get_clickhouse_client()
    # تبدیل تاریخ‌ها
    created_at = event['created_at']
    if isinstance(created_at, str):
        created_at = datetime.fromisoformat(created_at)
    closed_at = event.get('closed_at')
    if closed_at and isinstance(closed_at, str):
        closed_at = datetime.fromisoformat(closed_at)

    client.execute(
        f"INSERT INTO {settings.clickhouse_db}.issue_events "
        "(event_id, repo_id, repo_full_name, issue_number, title, state, author_username, category, priority, created_at, closed_at) "
        "VALUES",
        [(
            str(event.get('github_issue_id', '')),
            event['repo_id'],
            event['repo_full_name'],
            event['number'],
            event['title'],
            event['state'],
            event['author_username'],
            event.get('category', ''),
            event.get('priority', ''),
            created_at,
            closed_at
        )]
    )