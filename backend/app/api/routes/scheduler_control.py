from fastapi import APIRouter
from app.services.scheduler import scheduler, sync_all_repos
from datetime import datetime

router = APIRouter(prefix="/api/v1/scheduler", tags=["scheduler"])

# ذخیره‌ی زمان آخرین اجرا (ساده، در حافظه، با هر بار sync به‌روز می‌شود)
last_sync_time = None
auto_sync_enabled = True

@router.get("/status")
def get_scheduler_status():
    return {
        "auto_sync_enabled": auto_sync_enabled,
        "scheduler_running": scheduler.running,
        "last_sync_time": last_sync_time.isoformat() if last_sync_time else None
    }

@router.post("/trigger-sync")
def trigger_manual_sync():
    """اجرای فوری همگام‌سازی (بدون توجه به زمان‌بندی)"""
    sync_all_repos()  # این تابع در scheduler.py تعریف شده
    global last_sync_time
    last_sync_time = datetime.utcnow()
    return {"message": "Sync triggered successfully", "time": last_sync_time.isoformat()}

@router.post("/toggle-auto-sync")
def toggle_auto_sync():
    """روشن/خاموش کردن همگام‌سازی خودکار"""
    global auto_sync_enabled
    auto_sync_enabled = not auto_sync_enabled
    if auto_sync_enabled:
        # اگر job وجود نداشت دوباره اضافه کن
        if not scheduler.get_job('sync_all'):
            scheduler.add_job(sync_all_repos, 'interval', minutes=5, id='sync_all')
    else:
        if scheduler.get_job('sync_all'):
            scheduler.remove_job('sync_all')
    return {"auto_sync_enabled": auto_sync_enabled}