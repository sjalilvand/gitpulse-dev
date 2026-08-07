from sqlalchemy.orm import Session
from app.db.postgres import SessionLocal
from app.db.models.analytics import CommitAnalytics, IssueAnalytics
from datetime import datetime

def insert_commit_analytic(event: dict):
    db: Session = SessionLocal()
    try:
        committed_at = event['committed_at']
        if isinstance(committed_at, str):
            committed_at = datetime.fromisoformat(committed_at)
        rec = CommitAnalytics(
            repo_id=event['repo_id'],
            repo_full_name=event['repo_full_name'],
            commit_hash=event['commit_hash'],
            author_username=event['author_username'],
            branch=event.get('branch', 'main'),
            message=event['message'],
            additions=event.get('additions', 0),
            deletions=event.get('deletions', 0),
            files_changed=event.get('files_changed', 0),
            committed_at=committed_at
        )
        db.add(rec)
        db.commit()
        print(f"Saved commit analytic {event['commit_hash'][:8]}")
    except Exception as e:
        db.rollback()
        print(f"Error saving commit analytic: {e}")
    finally:
        db.close()

def insert_issue_analytic(event: dict):
    db: Session = SessionLocal()
    try:
        created_at = event['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        closed_at = event.get('closed_at')
        if closed_at and isinstance(closed_at, str):
            closed_at = datetime.fromisoformat(closed_at)
        rec = IssueAnalytics(
            repo_id=event['repo_id'],
            repo_full_name=event['repo_full_name'],
            github_issue_id=event['github_issue_id'],
            number=event['number'],
            title=event['title'],
            state=event['state'],
            author_username=event['author_username'],
            category=event.get('category', ''),
            priority=event.get('priority', ''),
            created_at=created_at,
            closed_at=closed_at
        )
        db.add(rec)
        db.commit()
        print(f"Saved issue analytic #{event['number']}")
    except Exception as e:
        db.rollback()
        print(f"Error saving issue analytic: {e}")
    finally:
        db.close()