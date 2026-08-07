import hashlib
import hmac
import json
from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.postgres import get_db
from app.db.models.repository import Repository
from app.services.kafka_service import send_event

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])

settings = get_settings()

def verify_signature(payload: bytes, signature: str):
    """بررسی صحت امضای وب‌هوک با secret"""
    if not settings.github_webhook_secret:
        return True  # اگر secret تنظیم نشده، رد نمی‌کنیم (فقط برای توسعه)
    expected = hmac.new(
        settings.github_webhook_secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    expected = f"sha256={expected}"
    return hmac.compare_digest(expected, signature)

@router.post("/github")
async def github_webhook(request: Request, db: Session = Depends(get_db)):
    # دریافت headerها
    event_type = request.headers.get("X-GitHub-Event")
    signature = request.headers.get("X-Hub-Signature-256", "")
    delivery = request.headers.get("X-GitHub-Delivery", "")

    # خواندن بدنه
    payload = await request.body()

    # اعتبارسنجی امضا
    if not verify_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = json.loads(payload)
    print(f"Received webhook: {event_type} (delivery={delivery})")

    if event_type == "push":
        # پردازش push (کامیت‌ها)
        repo_full_name = data["repository"]["full_name"]
        repo = db.query(Repository).filter(Repository.full_name == repo_full_name).first()
        if not repo:
            return {"status": "repo not tracked"}

        for commit in data.get("commits", []):
            event = {
                "repo_id": repo.id,
                "repo_full_name": repo_full_name,
                "commit_hash": commit["id"],
                "author_name": commit["author"]["name"],
                "author_email": commit["author"]["email"],
                "author_username": commit["author"].get("username", ""),
                "message": commit["message"],
                "branch": data["ref"].replace("refs/heads/", ""),
                "additions": commit.get("added", []).__len__(),  # arrays in push event
                "deletions": commit.get("removed", []).__len__(),
                "files_changed": commit.get("modified", []).__len__() + commit.get("added", []).__len__() + commit.get("removed", []).__len__(),
                "committed_at": commit["timestamp"],
            }
            send_event("github.commits.created", key=commit["id"], value=event)
        return {"status": "processed commits", "count": len(data.get("commits", []))}

    elif event_type == "pull_request":
        action = data["action"]
        pr = data["pull_request"]
        repo_full_name = data["repository"]["full_name"]
        repo = db.query(Repository).filter(Repository.full_name == repo_full_name).first()
        if not repo:
            return {"status": "repo not tracked"}

        # فقط برای PRهای باز یا sync شده (شامل open, synchronize)
        if action in ["opened", "synchronize"]:
            event = {
                "repo_id": repo.id,
                "repo_full_name": repo_full_name,
                "github_pr_id": pr["id"],
                "number": pr["number"],
                "title": pr["title"],
                "body": pr["body"] or "",
                "state": pr["state"],
                "author_username": pr["user"]["login"],
                "base_branch": pr["base"]["ref"],
                "head_branch": pr["head"]["ref"],
                "merged": pr["merged"],
                "merged_at": pr["merged_at"],
                "closed_at": pr["closed_at"],
                "created_at": pr["created_at"],
                "updated_at": pr["updated_at"],
                "additions": pr.get("additions", 0),
                "deletions": pr.get("deletions", 0),
                "changed_files": pr.get("changed_files", 0),
            }
            send_event("github.pull_requests.created", key=str(pr["id"]), value=event)
        return {"status": "processed PR"}

    elif event_type == "issues":
        action = data["action"]
        issue = data["issue"]
        repo_full_name = data["repository"]["full_name"]
        repo = db.query(Repository).filter(Repository.full_name == repo_full_name).first()
        if not repo:
            return {"status": "repo not tracked"}

        # فقط issueهای جدید یا ویرایش‌شده را پردازش می‌کنیم
        if action in ["opened", "edited"]:
            labels = ",".join([l["name"] for l in issue.get("labels", [])])
            event = {
                "repo_id": repo.id,
                "repo_full_name": repo_full_name,
                "github_issue_id": issue["id"],
                "number": issue["number"],
                "title": issue["title"],
                "body": issue["body"] or "",
                "state": issue["state"],
                "author_username": issue["user"]["login"],
                "labels": labels,
                "created_at": issue["created_at"],
                "updated_at": issue["updated_at"],
                "closed_at": issue["closed_at"],
            }
            send_event("github.issues.created", key=str(issue["id"]), value=event)
        return {"status": "processed issue"}

    return {"status": "event ignored"}