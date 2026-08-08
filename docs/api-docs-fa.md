```markdown
# مستندات API پلتفرم GitPulse AI

آدرس پایه: `http://localhost:8001/api/v1`

## نقاط پایانی (Endpoints)

### مخازن

| متد | مسیر | توضیح |
|------|------|--------|
| GET | `/repositories/` | لیست تمام مخازن |
| POST | `/repositories/` | افزودن مخزن جدید (بدنه: `{"url": "..."}`) |
| GET | `/repositories/{id}` | دریافت یک مخزن |
| POST | `/repositories/{id}/sync` | همگام‌سازی کامیت‌های مخزن |
| POST | `/repositories/{id}/sync-pr` | همگام‌سازی PRها |
| POST | `/repositories/{id}/sync-issues` | همگام‌سازی Issueها |

### کامیت‌ها

| متد | مسیر | توضیح |
|------|------|--------|
| GET | `/commits/?repo_id=1` | لیست کامیت‌ها (فیلتر اختیاری با repo_id) |

### درخواست‌های ادغام

| متد | مسیر | توضیح |
|------|------|--------|
| GET | `/pull-requests/?repo_id=1` | لیست PRها |

### مسائل

| متد | مسیر | توضیح |
|------|------|--------|
| GET | `/issues/?repo_id=1` | لیست Issueها |

### گزارش‌های هوش مصنوعی

| متد | مسیر | توضیح |
|------|------|--------|
| POST | `/ai/repositories/{id}/weekly-summary` | تولید خلاصه هفتگی |
| POST | `/ai/repositories/{id}/release-notes` | تولید یادداشت انتشار |
| POST | `/ai/pull-requests/{id}/risk-analysis` | تحلیل ریسک PR |
| POST | `/ai/issues/{id}/classify` | دسته‌بندی Issue |

### زمان‌بند

| متد | مسیر | توضیح |
|------|------|--------|
| GET | `/scheduler/status` | وضعیت همگام‌ساز |
| POST | `/scheduler/trigger-sync` | اجرای فوری همگام‌سازی |
| POST | `/scheduler/toggle-auto-sync` | روشن/خاموش کردن همگام‌سازی خودکار |

### Webhook

| متد | مسیر | توضیح |
|------|------|--------|
| POST | `/webhooks/github` | دریافت‌کننده webhook های GitHub (نیازمند تأیید امضا) |

## نمونه درخواست‌ها

### افزودن یک مخزن
```bash
curl -X POST http://localhost:8001/api/v1/repositories/ \
  -H "Content-Type: application/json" \
  -d '{"url":"https://github.com/fastapi/fastapi"}'
تولید خلاصه هفتگی
bash
curl -X POST http://localhost:8001/api/v1/ai/repositories/1/weekly-summary
اجرای همگام‌سازی دستی
bash
curl -X POST http://localhost:8001/api/v1/scheduler/trigger-sync