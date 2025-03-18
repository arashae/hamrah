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

### مدیریت تعاریف پایه

#### تعریف شرکت
- **URL**: `/api/management/define-company/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "name": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "name": "string"
}
```

#### تعریف فروشگاه
- **URL**: `/api/management/define-store/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "city_id": 0,
    "type": "string",
    "company_id": 0,
    "manager": "string",
    "phone_number": "string",
    "address": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "username": "string",
    "name": "string",
    "city": "string",
    "type": "string",
    "company": "string",
    "manager": "string",
    "phone_number": "string",
    "address": "string"
}
```

#### تعریف برند
- **URL**: `/api/management/define-brand/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "brand": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "brand": "string"
}
```

#### تعریف نوع دستگاه
- **URL**: `/api/management/define-type/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "category": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "category": "string"
}
```

#### تعریف طرح سهم‌بندی
- **URL**: `/api/management/define-portion-plan/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "category_id": 0,
    "MCI_portion": 0.0,
    "store_portion": 0.0,
    "supplier_portion": 0.0
}
```
- **Response**:
```json
{
    "id": 0,
    "category": "string",
    "MCI_portion": 0.0,
    "store_portion": 0.0,
    "supplier_portion": 0.0
}
```

#### تعریف دستگاه
- **URL**: `/api/management/define-device/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "category_id": 0,
    "brand_id": 0,
    "model": "string",
    "RAM": "string",
    "storage": "string",
    "color": "string",
    "pack": "string",
    "network": "string",
    "is_active": true
}
```
- **Response**:
```json
{
    "id": 0,
    "category": "string",
    "brand": "string",
    "model": "string",
    "RAM": "string",
    "storage": "string",
    "color": "string",
    "pack": "string",
    "network": "string",
    "is_active": true
}
```

#### تعریف ادمین
- **URL**: `/api/management/define-admin/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "role": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "username": "string",
    "name": "string",
    "role": "string"
}
```

#### تعریف تامین‌کننده
- **URL**: `/api/management/define-supplier/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Data**:
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "phone_number": "string",
    "is_active": true
}
```
- **Response**:
```json
{
    "id": 0,
    "username": "string",
    "name": "string",
    "phone_number": "string",
    "is_active": true
}
```

### مدیریت موجودی

#### ثبت موجودی جدید
- **URL**: `/api/inventory/inventory/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `inventory`
- **Data**:
```json
{
    "store_id": 0,
    "SKU_id": 0,
    "IMEI": "string",
    "receive_date": "datetime",
    "submit_date": "datetime",
    "discount_rate": 0.0,
    "status": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "store": "string",
    "SKU": "string",
    "IMEI": "string",
    "receive_date": "datetime",
    "submit_date": "datetime",
    "discount_rate": 0.0,
    "status": "string"
}
```

### مدیریت سفارشات

#### ثبت سفارش جدید
- **URL**: `/api/orders/orders/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `seller`
- **Data**:
```json
{
    "customer": {
        "first_name": "string",
        "last_name": "string",
        "national_code": "string",
        "phone_number": "string",
        "gender": true,
        "id_card": "string",
        "address": "string",
        "postal_code": "string"
    },
    "seller_id": 0,
    "transaction_id": "string",
    "is_full_cash": true,
    "loan_id": 0,
    "individual_discount_id": 0,
    "group_discount_id": 0,
    "items": [
        {
            "inventory_id": 0
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
    "order_date": "datetime",
    "transaction_id": "string",
    "is_full_cash": true,
    "loan": "string",
    "individual_discount": "string",
    "group_discount": "string",
    "items": [
        {
            "id": 0,
            "inventory": "string",
            "price": 0
        }
    ]
}
```

### گزارش‌ها

#### گزارش وضعیت انبار فروشگاه
- **URL**: `/api/reports/store-inventory/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin, seller`
- **Query Parameters**:
  - `store_id`: شناسه فروشگاه
  - `from_date`: از تاریخ
  - `to_date`: تا تاریخ
- **Response**:
```json
{
    "store": "string",
    "total_items": 0,
    "available_items": 0,
    "sold_items": 0,
    "items": [
        {
            "SKU": "string",
            "count": 0,
            "status": "string"
        }
    ]
}
```

#### گزارش وضعیت کلی فروشگاه‌ها
- **URL**: `/api/reports/all-stores/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Query Parameters**:
  - `from_date`: از تاریخ
  - `to_date`: تا تاریخ
- **Response**:
```json
{
    "total_stores": 0,
    "active_stores": 0,
    "stores": [
        {
            "name": "string",
            "total_sales": 0,
            "total_inventory": 0,
            "performance_rate": 0.0
        }
    ]
}
```

#### گزارش موجودی در گردش
- **URL**: `/api/reports/inventory-circulation/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin, inventory`
- **Query Parameters**:
  - `from_date`: از تاریخ
  - `to_date`: تا تاریخ
- **Response**:
```json
{
    "total_items": 0,
    "total_value": 0,
    "items": [
        {
            "SKU": "string",
            "count": 0,
            "value": 0,
            "circulation_days": 0
        }
    ]
}
```

#### گزارش مالی
- **URL**: `/api/reports/financial/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `admin`
- **Query Parameters**:
  - `from_date`: از تاریخ
  - `to_date`: تا تاریخ
  - `store_id`: شناسه فروشگاه (اختیاری)
- **Response**:
```json
{
    "total_sales": 0,
    "total_profit": 0,
    "total_discount": 0,
    "total_loan": 0,
    "portions": {
        "MCI": 0.0,
        "store": 0.0,
        "supplier": 0.0
    },
    "daily_report": [
        {
            "date": "date",
            "sales": 0,
            "profit": 0
        }
    ]
}
```

### مدیریت کاربران فروشگاه

#### ایجاد ادمین فروشگاه
- **URL**: `/api/accounts/store-admins/create/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `super_admin`
- **Data**:
```json
{
    "username": "string",
    "password": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "store": 0
}
```
- **Response**:
```json
{
    "id": 0,
    "username": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "role": "store_admin",
    "role_display": "ادمین فروشگاه",
    "store": 0,
    "store_name": "string",
    "is_active": true
}
```

#### لیست ادمین‌های فروشگاه
- **URL**: `/api/accounts/store-admins/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `super_admin`
- **Response**:
```json
[
    {
        "id": 0,
        "username": "string",
        "full_name": "string",
        "phone": "string",
        "national_code": "string",
        "role": "store_admin",
        "role_display": "ادمین فروشگاه",
        "store": 0,
        "store_name": "string",
        "is_active": true
    }
]
```

#### تغییر وضعیت ادمین فروشگاه
- **URL**: `/api/accounts/store-admins/<id>/toggle-status/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `super_admin`
- **Response**:
```json
{
    "status": "success",
    "is_active": true
}
```

#### ایجاد کاربر فروشگاه
- **URL**: `/api/accounts/store-users/create/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `store_admin`
- **Data**:
```json
{
    "username": "string",
    "password": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string"
}
```
- **Response**:
```json
{
    "id": 0,
    "username": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "role": "seller",
    "role_display": "فروشنده",
    "store": 0,
    "store_name": "string",
    "is_active": true
}
```

#### لیست کاربران فروشگاه
- **URL**: `/api/accounts/store-users/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `store_admin`
- **Response**:
```json
[
    {
        "id": 0,
        "username": "string",
        "full_name": "string",
        "phone": "string",
        "national_code": "string",
        "role": "seller",
        "role_display": "فروشنده",
        "store": 0,
        "store_name": "string",
        "is_active": true
    }
]
```

#### تغییر وضعیت کاربر فروشگاه
- **URL**: `/api/accounts/store-users/<id>/toggle-status/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Permissions**: `store_admin`
- **Response**:
```json
{
    "status": "success",
    "is_active": true
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
