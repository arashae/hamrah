from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, StoreAdmin, StoreUser, Customer
from management.models import Store, City, Province, Company, Supplier

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
        
        # ایجاد کاربر فروشنده
        self.seller_user = User.objects.create_user(
            username='seller',
            password='seller123',
            full_name='فروشنده تست',
            phone='09123456790',
            national_code='1234567891',
            role='seller',
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
        
        # دریافت توکن برای فروشنده
        self.seller_token = self.client.post(
            reverse('token_obtain'),
            {'username': 'seller', 'password': 'seller123'}
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
            role='seller',
            store=self.store
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

    # تست‌های مدیریت مشتریان
    def test_create_customer(self):
        """تست ایجاد مشتری جدید"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        data = {
            'first_name': 'علی',
            'last_name': 'محمدی',
            'national_code': '1234567894',
            'phone_number': '09123456793',
            'gender': True,
            'id_card': '123456789',
            'address': 'آدرس تست',
            'postal_code': '1234567890'
        }
        response = self.client.post(reverse('customer-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'علی')

    def test_list_customers(self):
        """تست لیست مشتریان"""
        # ایجاد مشتری تست
        Customer.objects.create(
            first_name='علی',
            last_name='محمدی',
            national_code='1234567894',
            phone_number='09123456793',
            gender=True,
            id_card='123456789',
            address='آدرس تست',
            postal_code='1234567890'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_update_customer(self):
        """تست ویرایش مشتری"""
        # ایجاد مشتری تست
        customer = Customer.objects.create(
            first_name='علی',
            last_name='محمدی',
            national_code='1234567894',
            phone_number='09123456793',
            gender=True,
            id_card='123456789',
            address='آدرس تست',
            postal_code='1234567890'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        data = {
            'first_name': 'علی',
            'last_name': 'احمدی',
            'national_code': '1234567894',
            'phone_number': '09123456793',
            'gender': True,
            'id_card': '123456789',
            'address': 'آدرس جدید',
            'postal_code': '1234567890'
        }
        response = self.client.put(reverse('customer-detail', kwargs={'pk': customer.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['last_name'], 'احمدی')

    def test_delete_customer(self):
        """تست حذف مشتری"""
        # ایجاد مشتری تست
        customer = Customer.objects.create(
            first_name='علی',
            last_name='محمدی',
            national_code='1234567894',
            phone_number='09123456793',
            gender=True,
            id_card='123456789',
            address='آدرس تست',
            postal_code='1234567890'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        response = self.client.delete(reverse('customer-detail', kwargs={'pk': customer.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    # تست‌های مدیریت تامین‌کنندگان
    def test_create_supplier(self):
        """تست ایجاد تامین‌کننده جدید"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        data = {
            'username': 'newsupplier',
            'password': 'supplier123',
            'name': 'تامین‌کننده جدید',
            'phone_number': '09123456794'
        }
        response = self.client.post(
            reverse('define-supplier'),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newsupplier')

    def test_list_suppliers(self):
        """تست لیست تامین‌کنندگان"""
        # ایجاد تامین‌کننده تست
        Supplier.objects.create(
            username='testsupplier',
            password='test123',
            name='تامین‌کننده تست',
            phone_number='09123456795'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.get(reverse('search-suppliers'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_update_supplier(self):
        """تست ویرایش تامین‌کننده"""
        # ایجاد تامین‌کننده تست
        supplier = Supplier.objects.create(
            username='testsupplier',
            password='test123',
            name='تامین‌کننده تست',
            phone_number='09123456795'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        data = {
            'name': 'تامین‌کننده بروز شده',
            'phone_number': '09123456796'
        }
        response = self.client.put(
            reverse('define-supplier-detail', kwargs={'supplier_id': supplier.id}),
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'تامین‌کننده بروز شده')

    def test_delete_supplier(self):
        """تست حذف تامین‌کننده"""
        # ایجاد تامین‌کننده تست
        supplier = Supplier.objects.create(
            username='testsupplier',
            password='test123',
            name='تامین‌کننده تست',
            phone_number='09123456795'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.delete(
            reverse('define-supplier-detail', kwargs={'supplier_id': supplier.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Supplier.objects.count(), 0)

    def test_toggle_supplier_status(self):
        """تست فعال/غیرفعال کردن تامین‌کننده"""
        # ایجاد تامین‌کننده تست
        supplier = Supplier.objects.create(
            username='testsupplier',
            password='test123',
            name='تامین‌کننده تست',
            phone_number='09123456795'
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        response = self.client.post(
            reverse('toggle-supplier-status', kwargs={'supplier_id': supplier.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('is_active', response.data)

    # تست‌های مدیریت پروفایل کاربر
    def test_get_user_profile(self):
        """تست دریافت پروفایل کاربر"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'storeadmin')

    def test_update_user_profile(self):
        """تست ویرایش پروفایل کاربر"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        data = {
            'full_name': 'ادمین جدید',
            'phone': '09123456795',
            'national_code': '1234567895'
        }
        response = self.client.put(reverse('user-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'ادمین جدید')

    def test_change_password(self):
        """تست تغییر رمز عبور"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.store_admin_token}')
        data = {
            'old_password': 'storeadmin123',
            'new_password': 'newpassword123'
        }
        response = self.client.post(reverse('change-password'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # تست ورود با رمز جدید
        token_response = self.client.post(
            reverse('token_obtain'),
            {'username': 'storeadmin', 'password': 'newpassword123'}
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK) 