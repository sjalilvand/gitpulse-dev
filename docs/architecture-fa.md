# معماری GitPulse AI

## نمای کلی

GitPulse AI از **معماری میکروسرویس رویدادمحور** با Apache Kafka به عنوان پیام‌رسان مرکزی استفاده می‌کند. این سیستم داده‌های GitHub را از طریق API polling یا webhook دریافت کرده، توسط workerهای اختصاصی پردازش می‌کند و در PostgreSQL (داده‌های عملیاتی) و ClickHouse (داده‌های تحلیلی) ذخیره می‌نماید. یک فرانت React و Grafana بصری‌سازی و تحلیل‌های هوشمند مبتنی بر AI را فراهم می‌کنند.

## نمودار سطح بالا
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
├─── AI Worker ──────────> PostgreSQL (گزارش‌ها)
│
▼
React Frontend Grafana

text

## جزئیات کامپوننت‌ها

### 1. API بک‌اند (FastAPI)
- مدیریت مخازن (CRUD).
- شروع همگام‌سازی دستی.
- دریافت و مدیریت webhook های GitHub (اختیاری).
- ارائه REST endpoint برای فرانت‌اند.
- انتشار رویدادها به topicهای Kafka.

### 2. Apache Kafka
- **Topicها**:
  - `github.commits.created`
  - `github.pull_requests.created`
  - `github.issues.created`
- **پیکربندی**: حالت KRaft (بدون Zookeeper).
- **ایجاد خودکار topic** برای محیط توسعه فعال است.

### 3. Workerها (مصرف‌کننده‌های Python)
- **Commit Worker**: رویدادهای کامیت را ذخیره می‌کند.
- **PR Worker**: درخواست‌های ادغام را ذخیره و امتیاز ریسک اولیه می‌دهد.
- **Issue Worker**: مسائل را ذخیره و برای دسته‌بندی آماده می‌کند.
- **Analytics Worker**: داده‌ها را در جداول ClickHouse تجمیع می‌کند.
- **AI Worker**: گزارش‌های AI را با AvalAI تولید می‌کند.

همه workerها مستقل هستند و می‌توانند جداگانه مقیاس‌پذیر باشند.

### 4. پایگاه‌های داده
- **PostgreSQL**: مخزن عملیاتی اصلی. جداول: `repositories`, `commits`, `pull_requests`, `issues`, `commit_analytics`, `issue_analytics`, `ai_reports`.
- **ClickHouse**: مخزن تحلیلی با کارایی بالا. جداول: `commit_events`, `issue_events`. بهینه‌سازی شده برای تجمیع سری زمانی.

### 5. فرانت‌اند (React)
- ساخته شده با Vite, TypeScript, TailwindCSS, Recharts.
- صفحات: داشبورد، لیست مخازن، جزئیات مخزن (تب‌ها: کامیت‌ها، PRها، مسائل، گزارش‌های AI).
- بخش گزارش‌های AI شامل خلاصه هفتگی، تحلیل ریسک PR و تولید Release Notes است.
- صفحه تنظیمات برای کنترل همگام‌ساز.

### 6. Grafana
- متصل به PostgreSQL برای داشبوردهای تحلیلی.
- پنل‌ها: فعالیت کامیت‌ها در طول زمان، مشارکت‌کنندگان برتر، توزیع وضعیت Issue.
- (قابل گسترش) می‌تواند برای داده‌های حجیم به ClickHouse متصل شود.

### 7. زمان‌بند پس‌زمینه
- APScheduler درون بک‌اند هر ۵ دقیقه کامیت‌ها، PRها و Issueهای جدید را از GitHub دریافت می‌کند.
- از طریق API و UI قابل فعال/غیرفعال کردن است.

## جریان داده‌ها

1. کاربر یک مخزن GitHub را از طریق فرانت اضافه می‌کند → بک‌اند متادیتا را ذخیره می‌کند.
2. با همگام‌سازی دستی یا خودکار، بک‌اند با PyGithub داده‌های اخیر را دریافت می‌کند.
3. هر آیتم به عنوان یک رویداد در topic مناسب Kafka منتشر می‌شود.
4. Workerها رویدادها را مصرف و در PostgreSQL و ClickHouse ذخیره می‌کنند.
5. Analytics Worker داده‌های تجمیعی را برای Grafana به ClickHouse می‌فرستد.
6. AI Worker (یا API درخواستی) برای تولید خلاصه، تحلیل ریسک و ... از AvalAI استفاده می‌کند.
7. فرانت‌اند APIهای REST را برای نمایش داده‌ها فراخوانی می‌کند.

## استقرار

- Docker Compose همه سرویس‌ها را مدیریت می‌کند.
- `docker-compose.yml` شامل PostgreSQL، ClickHouse، Kafka، Backend، Frontend، Grafana و کانتینرهای worker است.
- متغیرهای محیطی از طریق فایل `.env` مدیریت می‌شوند.