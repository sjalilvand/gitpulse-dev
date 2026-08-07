from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.postgres import SessionLocal
from app.db.models.repository import Repository
from app.services.github_service import get_github_client
from app.services.kafka_service import send_event
from datetime import datetime, timezone
import time
last_sync_time = None  # زمان آخرین همگام‌سازی


def sync_all_repos():
    """تمام مخازن را بررسی کرده و رویدادهای جدید را ارسال می‌کند"""
    db: Session = SessionLocal()
    try:
        repos = db.query(Repository).all()
        for repo in repos:
            print(f"Syncing {repo.full_name}...")
            try:
                client = get_github_client()
                gh_repo = client.get_repo(repo.full_name)

                # ۱. کامیت‌های جدید (اخیراً push شده)
                commits = gh_repo.get_commits(
                    since=datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0))  # یک ساعت اخیر
                for commit in commits:
                    event = {
                        "repo_id": repo.id,
                        "repo_full_name": repo.full_name,
                        "commit_hash": commit.sha,
                        "author_name": commit.commit.author.name,
                        "author_email": commit.commit.author.email,
                        "author_username": commit.author.login if commit.author else "",
                        "message": commit.commit.message,
                        "branch": repo.default_branch,
                        "additions": commit.stats.additions if commit.stats else 0,
                        "deletions": commit.stats.deletions if commit.stats else 0,
                        "files_changed": commit.stats.total if commit.stats else 0,
                        "committed_at": commit.commit.author.date.isoformat()
                    }
                    send_event("github.commits.created", key=commit.sha, value=event)

                # ۲. PRهای جدید (اخیراً به‌روزرسانی شده)
                pulls = gh_repo.get_pulls(state='all', sort='updated', direction='desc')[:5]
                for pr in pulls:
                    # ارسال به عنوان رویداد PR
                    event = {
                        "repo_id": repo.id,
                        "repo_full_name": repo.full_name,
                        "github_pr_id": pr.id,
                        "number": pr.number,
                        "title": pr.title,
                        "body": pr.body or "",
                        "state": pr.state,
                        "author_username": pr.user.login,
                        "base_branch": pr.base.ref,
                        "head_branch": pr.head.ref,
                        "merged": pr.merged,
                        "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                        "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                        "created_at": pr.created_at.isoformat(),
                        "updated_at": pr.updated_at.isoformat(),
                        "additions": pr.additions,
                        "deletions": pr.deletions,
                        "changed_files": pr.changed_files,
                    }
                    send_event("github.pull_requests.created", key=str(pr.id), value=event)

                # ۳. Issueهای جدید
                issues = gh_repo.get_issues(state='all', sort='updated', direction='desc')[:5]
                for issue in issues:
                    if issue.pull_request:  # PRها را نادیده می‌گیریم
                        continue
                    event = {
                        "repo_id": repo.id,
                        "repo_full_name": repo.full_name,
                        "github_issue_id": issue.id,
                        "number": issue.number,
                        "title": issue.title,
                        "body": issue.body or "",
                        "state": issue.state,
                        "author_username": issue.user.login,
                        "labels": ",".join([l.name for l in issue.labels]),
                        "created_at": issue.created_at.isoformat(),
                        "updated_at": issue.updated_at.isoformat(),
                        "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    }
                    send_event("github.issues.created", key=str(issue.id), value=event)

            except Exception as e:
                print(f"Error syncing {repo.full_name}: {e}")
    finally:
        global last_sync_time
        last_sync_time = datetime.utcnow()
        db.close()


# راه‌اندازی scheduler
scheduler = BackgroundScheduler()


def start_scheduler():
    # هر ۵ دقیقه یک‌بار اجرا شود
    scheduler.add_job(sync_all_repos, 'interval', minutes=5, id='sync_all')
    scheduler.start()
    print("Scheduler started (sync every 5 minutes).")


def stop_scheduler():
    scheduler.shutdown()