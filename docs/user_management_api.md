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
    "refresh": "string"
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
    "is_active": true
  }
  ```

### لیست ادمین‌های فروشگاه
- **URL:** `/api/accounts/store-admin/list/`
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
- **URL:** `/api/accounts/store-admin/{admin_id}/toggle-status/`
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
- **URL:** `/api/accounts/store-user/create/`
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
    "is_active": true
  }
  ```

### لیست کاربران فروشگاه
- **URL:** `/api/accounts/store-user/list/`
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
      "is_active": true
    }
  ]
  ```

### فعال/غیرفعال کردن کاربر فروشگاه
- **URL:** `/api/accounts/store-user/{user_id}/toggle-status/`
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