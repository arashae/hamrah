# سیستم مدیریت فروشگاه همراه

این پروژه یک سیستم مدیریت فروشگاه موبایل است که با استفاده از Django REST framework و SQLite توسعه داده شده است.

## ویژگی‌های اصلی

- مدیریت کاربران و احراز هویت با JWT
- مدیریت فروشگاه‌ها و موجودی
- مدیریت سفارشات و تخفیف‌ها
- سیستم وام و پرداخت
- مستندات API با Swagger
- سیستم لاگینگ
- تست‌های واحد

## نصب و راه‌اندازی

1. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

2. اجرای مایگریشن‌ها:
```bash
python manage.py migrate
```

3. ایجاد کاربر ادمین:
```bash
python manage.py createsuperuser
```

4. اجرای سرور:
```bash
python manage.py runserver
```

## مستندات API

پس از اجرای سرور، می‌توانید مستندات API را در آدرس‌های زیر مشاهده کنید:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## تست‌ها

برای اجرای تست‌ها:
```bash
python manage.py test
```

## توسعه‌دهنده

- نام: Arash
- ایمیل: slamiarash@gmail.com
- شماره تماس: 09391477665
