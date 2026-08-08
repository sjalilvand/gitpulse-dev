# راهنمای نصب و راه‌اندازی GitPulse AI

## پیش‌نیازها

- **Docker** و **Docker Compose** (نسخه ۲ به بالا)
- **Git**
- یک **توکن دسترسی شخصی GitHub** (classic) با دسترسی `public_repo` (یا `repo` برای مخازن خصوصی).
- یک **کلید API آوالای** (یا هر endpoint سازگار با OpenAI) – اختیاری اما برای قابلیت‌های AI توصیه می‌شود.

## مراحل نصب

### ۱. دریافت کد منبع
```bash
git clone https://github.com/sjalilvand/gitpulse-dev.git
cd gitpulse-ai
۲. تنظیم متغیرهای محیطی
bash
cp .env.example .env
فایل .env را ویرایش کنید و مقادیر زیر را تنظیم نمایید:

GITHUB_TOKEN: توکن دسترسی شخصی GitHub شما.

AVALAI_API_KEY: کلید API آوالای (در صورت استفاده از AI).

AVALAI_BASE_URL: https://api.avalai.ir/v1 (یا endpoint دلخواه).

GITHUB_WEBHOOK_SECRET: یک رشته تصادفی (در صورت استفاده از webhook).

(سایر متغیرها از پیش تنظیم شده‌اند.)

۳. اجرای سرویس‌ها
bash
docker compose up -d
حدود یک دقیقه صبر کنید تا همه کانتینرها سالم شوند. برای بررسی وضعیت:

bash
docker compose ps
۴. دسترسی به برنامه
فرانت‌اند: http://localhost:5173

API بک‌اند: http://localhost:8001/health

Grafana: http://localhost:3000 (نام کاربری: admin، رمز عبور: admin)

ClickHouse Playground: http://localhost:8123/play

افزودن اولین مخزن
فرانت‌اند را باز کنید → روی مخازن کلیک کنید.

یک آدرس مخزن GitHub وارد کنید (مثلاً https://github.com/fastapi/fastapi).

مخزن اضافه شده و مشخصات آن نمایش داده می‌شود.

برای همگام‌سازی کامیت‌ها/PRها/Issueها:

به صفحه جزئیات مخزن بروید و از دکمه‌های "Sync" استفاده کنید (دستی)، یا

منتظر بمانید تا زمان‌بند خودکار (هر ۵ دقیقه) داده‌ها را بروز کند، یا

از صفحه تنظیمات برای اجرای همگام‌سازی دستی کامل استفاده کنید.

فعال‌سازی قابلیت‌های هوش مصنوعی
مطمئن شوید فایل .env شامل یک AVALAI_API_KEY معتبر است. قابلیت‌های AI (خلاصه هفتگی، تحلیل ریسک PR، یادداشت انتشار) در تب گزارش‌های هوش مصنوعی هر مخزن در دسترس خواهند بود.

راه‌اندازی داشبوردهای Grafana
با admin/admin وارد Grafana شوید.

به Data Sources رفته و یک PostgreSQL جدید اضافه کنید.

Host: postgres:5432

Database: gitpulse

User: gitpulse

Password: gitpulse123

SSL: غیرفعال

یک داشبورد جدید با پنل‌هایی از جداول commit_analytics و issue_analytics بسازید.

رفع اشکالات رایج
عدم اتصال به Docker Hub: یک پروکسی در تنظیمات Docker Desktop تنظیم کنید یا از mirror داخلی استفاده کنید.

بک‌اند اجرا نمی‌شود: لاگ‌ها را با docker logs gitpulse-backend بررسی کنید. از صحت توکن GitHub مطمئن شوید.

خطای workerها: لاگ worker مربوطه را ببینید (docker logs gitpulse-commit-worker و ...).

تداخل پورت: پورت‌های در معرض دید را در docker-compose.yml تغییر دهید.

توقف پروژه
bash
docker compose down
(با افزودن -v volumeها نیز حذف می‌شوند – دقت کنید داده‌ها از بین می‌روند.)

توسعه
کد بک‌اند به صورت volume مانت شده و تغییرات به‌طور خودکار بارگذاری می‌شود.

فرانت‌اند از HMR ویت استفاده می‌کند؛ مرورگر را رفرش کنید.

برای نصب وابستگی‌های جدید پایتون، docker compose up -d --build backend را اجرا کنید.