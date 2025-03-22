# API های مدیریت کاربران

## احراز هویت

### دریافت توکن
- **URL:** `/api/accounts/token/`
- **Method:** `POST`
- **دسترسی:** عمومی
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "access": "string",
    "refresh": "string",
    "user": {
      "id": "integer",
      "username": "string",
      "full_name": "string",
      "role": "string",
      "role_display": "string",
      "store": "integer",
      "store_name": "string"
    }
  }
  ```

### تمدید توکن
- **URL:** `/api/accounts/token/refresh/`
- **Method:** `POST`
- **دسترسی:** عمومی
- **Body:**
  ```json
  {
    "refresh": "string"
  }
  ```
- **Response:**
  ```json
  {
    "access": "string"
  }
  ```

## مدیریت کاربران توسط سوپر ادمین

### ایجاد ادمین فروشگاه
- **URL:** `/api/accounts/store-admin/create/`
- **Method:** `POST`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "store": "integer"
  }
  ```
- **Response:**
  ```json
  {
    "id": "integer",
    "username": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "store": "integer",
    "store_name": "string",
    "is_active": true
  }
  ```

### لیست ادمین‌های فروشگاه
- **URL:** `/api/accounts/store-admins/`
- **Method:** `GET`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Response:**
  ```json
  [
    {
      "id": "integer",
      "username": "string",
      "full_name": "string",
      "phone": "string",
      "national_code": "string",
      "store": "integer",
      "store_name": "string",
      "is_active": true
    }
  ]
  ```

### فعال/غیرفعال کردن ادمین فروشگاه
- **URL:** `/api/accounts/store-admins/{admin_id}/toggle-status/`
- **Method:** `POST`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Response:**
  ```json
  {
    "status": "success",
    "is_active": true
  }
  ```

## مدیریت کاربران توسط ادمین فروشگاه

### ایجاد کاربر فروشگاه (فروشنده/انباردار)
- **URL:** `/api/accounts/store-users/create/`
- **Method:** `POST`
- **دسترسی:** فقط ادمین فروشگاه
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "role": "seller|warehouse"
  }
  ```
- **Response:**
  ```json
  {
    "id": "integer",
    "username": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "role": "string",
    "role_display": "string",
    "store": "integer",
    "store_name": "string",
    "is_active": true
  }
  ```

### لیست کاربران فروشگاه
- **URL:** `/api/accounts/store-users/`
- **Method:** `GET`
- **دسترسی:** فقط ادمین فروشگاه
- **Headers:** `Authorization: Bearer {token}`
- **Response:**
  ```json
  [
    {
      "id": "integer",
      "username": "string",
      "full_name": "string",
      "phone": "string",
      "national_code": "string",
      "role": "string",
      "role_display": "string",
      "store": "integer",
      "store_name": "string",
      "is_active": true
    }
  ]
  ```

### فعال/غیرفعال کردن کاربر فروشگاه
- **URL:** `/api/accounts/store-users/{user_id}/toggle-status/`
- **Method:** `POST`
- **دسترسی:** فقط ادمین فروشگاه
- **Headers:** `Authorization: Bearer {token}`
- **Response:**
  ```json
  {
    "status": "success",
    "is_active": true
  }
  ```

## مدیریت مشتریان

### لیست مشتریان
- **URL:** `/api/accounts/customers/`
- **Method:** `GET`
- **دسترسی:** ادمین و فروشنده
- **Headers:** `Authorization: Bearer {token}`
- **Query Parameters:**
  - `national_code`: جستجو بر اساس کد ملی
  - `phone_number`: جستجو بر اساس شماره تلفن
  - `name`: جستجو بر اساس نام
- **Response:**
  ```json
  [
    {
      "id": "integer",
      "first_name": "string",
      "last_name": "string",
      "national_code": "string",
      "phone_number": "string",
      "gender": true,
      "id_card": "string",
      "address": "string",
      "postal_code": "string"
    }
  ]
  ```

### ایجاد مشتری جدید
- **URL:** `/api/accounts/customers/`
- **Method:** `POST`
- **دسترسی:** ادمین و فروشنده
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "national_code": "string",
    "phone_number": "string",
    "gender": true,
    "id_card": "string",
    "address": "string",
    "postal_code": "string"
  }
  ```

### ویرایش مشتری
- **URL:** `/api/accounts/customers/{id}/`
- **Method:** `PUT`
- **دسترسی:** ادمین و فروشنده
- **Headers:** `Authorization: Bearer {token}`
- **Body:** مشابه ایجاد مشتری

### حذف مشتری
- **URL:** `/api/accounts/customers/{id}/`
- **Method:** `DELETE`
- **دسترسی:** ادمین و فروشنده
- **Headers:** `Authorization: Bearer {token}`

## مدیریت تامین‌کنندگان

### ایجاد تامین‌کننده جدید
- **URL:** `/api/management/suppliers/define/`
- **Method:** `POST`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "name": "string",
    "phone_number": "string"
  }
  ```
- **Response:**
  ```json
  {
    "id": "integer",
    "username": "string",
    "name": "string",
    "phone_number": "string",
    "is_active": true
  }
  ```

### لیست تامین‌کنندگان
- **URL:** `/api/management/suppliers/search/`
- **Method:** `GET`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Query Parameters:**
  - `name`: جستجو بر اساس نام
  - `is_active`: فیلتر بر اساس وضعیت فعال/غیرفعال
- **Response:**
  ```json
  [
    {
      "id": "integer",
      "username": "string",
      "name": "string",
      "phone_number": "string",
      "is_active": true
    }
  ]
  ```

### ویرایش تامین‌کننده
- **URL:** `/api/management/suppliers/define/`
- **Method:** `PUT`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "id": "integer",
    "name": "string",
    "phone_number": "string"
  }
  ```
- **Response:**
  ```json
  {
    "id": "integer",
    "username": "string",
    "name": "string",
    "phone_number": "string",
    "is_active": true
  }
  ```

### حذف تامین‌کننده
- **URL:** `/api/management/suppliers/define/`
- **Method:** `DELETE`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "id": "integer"
  }
  ```
- **Response:** `204 No Content`

### فعال/غیرفعال کردن تامین‌کننده
- **URL:** `/api/management/suppliers/{supplier_id}/toggle-status/`
- **Method:** `POST`
- **دسترسی:** فقط سوپر ادمین
- **Headers:** `Authorization: Bearer {token}`
- **Response:**
  ```json
  {
    "status": "success",
    "is_active": true
  }
  ```

## مدیریت پروفایل کاربر

### نمایش پروفایل
- **URL:** `/api/accounts/profile/`
- **Method:** `GET`
- **دسترسی:** کاربر احراز هویت شده
- **Headers:** `Authorization: Bearer {token}`
- **Response:**
  ```json
  {
    "id": "integer",
    "username": "string",
    "full_name": "string",
    "phone": "string",
    "national_code": "string",
    "role": "string",
    "role_display": "string",
    "store": "integer",
    "store_name": "string",
    "is_active": true
  }
  ```

### ویرایش پروفایل
- **URL:** `/api/accounts/profile/`
- **Method:** `PUT/PATCH`
- **دسترسی:** کاربر احراز هویت شده
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "full_name": "string",
    "phone": "string",
    "national_code": "string"
  }
  ```

### تغییر رمز عبور
- **URL:** `/api/accounts/change-password/`
- **Method:** `POST`
- **دسترسی:** کاربر احراز هویت شده
- **Headers:** `Authorization: Bearer {token}`
- **Body:**
  ```json
  {
    "old_password": "string",
    "new_password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success"
  }
  ```

## کدهای خطا

- **400 Bad Request:** داده‌های ارسالی نامعتبر هستند
- **401 Unauthorized:** توکن احراز هویت ارائه نشده یا نامعتبر است
- **403 Forbidden:** کاربر دسترسی لازم را ندارد
- **404 Not Found:** کاربر مورد نظر یافت نشد

## نکات مهم

1. تمام درخواست‌ها (به جز دریافت و تمدید توکن) نیاز به ارسال توکن در هدر `Authorization` دارند.
2. فرمت توکن باید به صورت `Bearer {token}` باشد.
3. سوپر ادمین فقط می‌تواند ادمین فروشگاه ایجاد کند.
4. ادمین فروشگاه فقط می‌تواند فروشنده و انباردار برای فروشگاه خود ایجاد کند.
5. هر ادمین فروشگاه فقط به کاربران فروشگاه خود دسترسی دارد.
6. کد ملی و شماره تلفن باید در فرمت صحیح وارد شوند.
7. نام کاربری باید یکتا باشد.
8. رمز عبور باید حداقل 8 کاراکتر باشد.
9. مشتریان و تامین‌کنندگان باید کد ملی یکتا داشته باشند.
10. تمام عملیات در سیستم لاگ می‌شوند. 