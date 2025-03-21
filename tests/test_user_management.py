from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, StoreAdmin, StoreUser
from management.models import Store, City, Province, Company

class UserManagementAPITests(APITestCase):
    def setUp(self):
        # ایجاد سوپر ادمین
        self.superuser = User.objects.create_superuser(
            username='superadmin',
            password='superadmin123',
            full_name='سوپر ادمین',
            phone='09123456789',
            national_code='1234567890',
            role='superadmin'
        )
        
        # ایجاد داده‌های پایه
        self.province = Province.objects.create(province='تهران')
        self.city = City.objects.create(city='تهران', province=self.province)
        self.company = Company.objects.create(name='شرکت تست')
        
        # ایجاد فروشگاه
        self.store = Store.objects.create(
            username='teststore',
            password='store123',
            name='فروشگاه تست',
            city=self.city,
            type='retail',
            company=self.company,
            manager='مدیر تست',
            phone_number='09123456789',
            address='آدرس تست'
        )
        
        # ایجاد کاربر ادمین فروشگاه
        self.store_admin_user = User.objects.create_user(
            username='storeadmin',
            password='storeadmin123',
            full_name='ادمین فروشگاه',
            phone='09123456789',
            national_code='1234567890',
            role='store_admin',
            store=self.store
        )
        
        # ایجاد ادمین فروشگاه
        self.store_admin = StoreAdmin.objects.create(
            user=self.store_admin_user,
            store=self.store
        )
        
        # دریافت توکن برای سوپر ادمین
        self.superuser_token = self.client.post(
            reverse('token_obtain'),
            {'username': 'superadmin', 'password': 'superadmin123'}
        ).data['access']
        
        # دریافت توکن برای ادمین فروشگاه
        self.store_admin_token = self.client.post(
            reverse('token_obtain'),
            {'username': 'storeadmin', 'password': 'storeadmin123'}
        ).data['access']

    def test_token_obtain(self):
        """تست دریافت توکن"""
        response = self.client.post(
            reverse('token_obtain'),
            {'username': 'superadmin', 'password': 'superadmin123'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh(self):
        """تست تمدید توکن"""
        # دریافت توکن اولیه
        token_response = self.client.post(
            reverse('token_obtain'),
            {'username': 'superadmin', 'password': 'superadmin123'}
        )
        refresh_token = token_response.data['refresh']
        
        # تمدید توکن
        response = self.client.post(
            reverse('token_refresh'),
            {'refresh': refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_create_store_admin(self):
        """تست ایجاد ادمین فروشگاه توسط سوپر ادمین"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        data = {
            'username': 'newstoreadmin',
            'password': 'newadmin123',
            'full_name': 'ادمین جدید',
            'phone': '09123456790',
            'national_code': '1234567891',
            'store': self.store.id
        }
        response = self.client.post(
            reverse('create-store-admin'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newstoreadmin')

    def test_list_store_admins(self):
        """تست لیست ادمین‌های فروشگاه"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.get(reverse('store-admin-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_toggle_store_admin_status(self):
        """تست فعال/غیرفعال کردن ادمین فروشگاه"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.post(
            reverse('toggle-store-admin-status', kwargs={'admin_id': self.store_admin_user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_active', response.data)

    def test_create_store_user(self):
        """تست ایجاد کاربر فروشگاه توسط ادمین فروشگاه"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        data = {
            'username': 'newstoreuser',
            'password': 'newuser123',
            'full_name': 'کاربر جدید',
            'phone': '09123456791',
            'national_code': '1234567892',
            'role': 'seller'
        }
        response = self.client.post(
            reverse('create-store-user'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newstoreuser')

    def test_list_store_users(self):
        """تست لیست کاربران فروشگاه"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        response = self.client.get(reverse('store-user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_toggle_store_user_status(self):
        """تست فعال/غیرفعال کردن کاربر فروشگاه"""
        # ایجاد کاربر فروشگاه
        store_user_account = User.objects.create_user(
            username='teststoreuser',
            password='testuser123',
            full_name='کاربر تست',
            phone='09123456792',
            national_code='1234567893',
            role='seller'
        )
        store_user = StoreUser.objects.create(
            user=store_user_account,
            store=self.store,
            role='seller'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        response = self.client.post(
            reverse('toggle-store-user-status', kwargs={'user_id': store_user_account.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_active', response.data)

    def test_unauthorized_access(self):
        """تست دسترسی غیرمجاز"""
        # تست بدون توکن
        response = self.client.get(reverse('store-admin-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # تست با توکن نامعتبر
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(reverse('store-admin-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 