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

### احراز هویت

#### دریافت توکن JWT
- **URL**: `/api/token/`
- **Method**: `POST`
- **Data**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response**:
```json
{
    "access": "string",
    "refresh": "string"
}
```

#### بروزرسانی توکن
- **URL**: `/api/token/refresh/`
- **Method**: `POST`
- **Data**:
```json
{
    "refresh": "string"
}
```
- **Response**:
```json
{
    "access": "string"
}
```

### مدیریت فروشگاه‌ها

#### لیست فروشگاه‌ها
- **URL**: `/api/store/stores/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `city`: فیلتر بر اساس شهر
  - `type`: فیلتر بر اساس نوع فروشگاه
  - `company`: فیلتر بر اساس شرکت
- **Response**:
```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "name": "string",
            "city": "string",
            "type": "string",
            "company": "string",
            "manager": "string",
            "phone_number": "string",
            "address": "string"
        }
    ]
}
```

### مدیریت موجودی

#### لیست موجودی‌ها
- **URL**: `/api/inventory/inventory/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `store`: فیلتر بر اساس فروشگاه
  - `SKU`: فیلتر بر اساس SKU
  - `status`: فیلتر بر اساس وضعیت
- **Response**:
```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "store": "string",
            "SKU": "string",
            "IMEI": "string",
            "status": "string"
        }
    ]
}
```

### مدیریت سفارشات

#### ایجاد سفارش جدید
- **URL**: `/api/orders/orders/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Data**:
```json
{
    "customer": 0,
    "seller": 0,
    "transaction_id": "string",
    "is_full_cash": true,
    "group_discount": 0,
    "items": [
        {
            "inventory": 0
        }
    ]
}
```
- **Response**:
```json
{
    "id": 0,
    "customer": "string",
    "seller": "string",
    "transaction_id": "string",
    "is_full_cash": true,
    "group_discount": "string",
    "items": [
        {
            "id": 0,
            "order": 0,
            "inventory": "string",
            "price": 0
        }
    ]
}
```

#### لیست سفارشات
- **URL**: `/api/orders/orders/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `customer`: فیلتر بر اساس مشتری
  - `seller`: فیلتر بر اساس فروشنده
  - `is_full_cash`: فیلتر بر اساس نوع پرداخت
- **Response**:
```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "customer": "string",
            "seller": "string",
            "transaction_id": "string",
            "is_full_cash": true,
            "group_discount": "string",
            "items": [
                {
                    "id": 0,
                    "order": 0,
                    "inventory": "string",
                    "price": 0
                }
            ]
        }
    ]
}
```

### مدیریت تخفیف‌ها

#### لیست تخفیف‌های گروهی
- **URL**: `/api/orders/group-discounts/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `available`: فیلتر بر اساس در دسترس بودن
- **Response**:
```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "used_count": 0,
            "max_use": 0
        }
    ]
}
```

#### لیست تخفیف‌های فردی
- **URL**: `/api/orders/individual-discounts/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `customer`: فیلتر بر اساس مشتری
  - `active`: فیلتر بر اساس فعال بودن
- **Response**:
```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "active_date": "string",
            "customer": "string"
        }
    ]
}
```

### مدیریت وام‌ها

#### لیست وام‌ها
- **URL**: `/api/orders/loans/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response**:
```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {
            "id": 0,
            "prepayment": 0
        }
    ]
}
```

## تست‌ها

برای اجرای تست‌ها:
```bash
python manage.py test
```

## توسعه‌دهنده

- نام: Arash
- ایمیل: slamiarash@gmail.com
- شماره تماس: 09391477665
