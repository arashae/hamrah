from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from .models import IndividualDiscount, GroupDiscount, Loan, Order, OrderItem
from accounts.models import Customer, Seller
from inventory.models import Inventory, SKU, Device, Brand, Category, Supplier, Guarantee
from store.models import Store, City, Province, Company

class OrderTests(APITestCase):
    def setUp(self):
        # ایجاد داده‌های تست
        self.province = Province.objects.create(province='تهران')
        self.city = City.objects.create(city='تهران', province=self.province)
        self.company = Company.objects.create(name='شرکت تست')
        self.store = Store.objects.create(
            username='store1',
            password='test123',
            name='فروشگاه تست',
            city=self.city,
            type='regular',
            company=self.company,
            manager='مدیر تست',
            phone_number='09123456789',
            address='آدرس تست'
        )
        self.seller = Seller.objects.create(
            username='seller1',
            password='test123',
            name='فروشنده تست',
            store=self.store
        )
        self.customer = Customer.objects.create(
            first_name='نام',
            last_name='نام خانوادگی',
            national_code='1234567890',
            phone_number='09123456789',
            gender=True,
            id_card='1234567890',
            address='آدرس تست',
            postal_code='1234567890'
        )
        self.brand = Brand.objects.create(brand='برند تست')
        self.category = Category.objects.create(category='دسته تست')
        self.device = Device.objects.create(
            category=self.category,
            brand=self.brand,
            model='مدل تست',
            RAM='4GB',
            storage='64GB',
            color='مشکی',
            pack='کامل',
            network='4G'
        )
        self.supplier = Supplier.objects.create(
            username='supplier1',
            password='test123',
            name='تامین‌کننده تست'
        )
        self.guarantee = Guarantee.objects.create(guarantee='گارانتی تست')
        self.sku = SKU.objects.create(
            device=self.device,
            supplier=self.supplier,
            price=1000000,
            guarantee=self.guarantee
        )
        self.inventory = Inventory.objects.create(
            store=self.store,
            SKU=self.sku,
            IMEI='123456789012345',
            status='available'
        )
        self.group_discount = GroupDiscount.objects.create(
            used_count=0,
            max_use=10
        )
        self.individual_discount = IndividualDiscount.objects.create(
            active_date=timezone.now(),
            customer=self.customer
        )
        self.loan = Loan.objects.create(prepayment=100000)

    def test_create_order(self):
        """
        تست ایجاد سفارش جدید
        """
        url = reverse('order-list')
        data = {
            'customer': self.customer.id,
            'seller': self.seller.id,
            'transaction_id': '123456789012',
            'is_full_cash': True,
            'items': [
                {
                    'inventory': self.inventory.id
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        # بررسی وضعیت موجودی
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.status, 'sold')

    def test_create_order_with_unavailable_inventory(self):
        """
        تست ایجاد سفارش با موجودی ناموجود
        """
        self.inventory.status = 'sold'
        self.inventory.save()

        url = reverse('order-list')
        data = {
            'customer': self.customer.id,
            'seller': self.seller.id,
            'transaction_id': '123456789012',
            'is_full_cash': True,
            'items': [
                {
                    'inventory': self.inventory.id
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

    def test_create_order_with_group_discount(self):
        """
        تست ایجاد سفارش با تخفیف گروهی
        """
        url = reverse('order-list')
        data = {
            'customer': self.customer.id,
            'seller': self.seller.id,
            'transaction_id': '123456789012',
            'is_full_cash': True,
            'group_discount': self.group_discount.id,
            'items': [
                {
                    'inventory': self.inventory.id
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # بررسی به‌روزرسانی تخفیف گروهی
        self.group_discount.refresh_from_db()
        self.assertEqual(self.group_discount.used_count, 1)

    def test_delete_order(self):
        """
        تست حذف سفارش
        """
        # ایجاد سفارش
        order = Order.objects.create(
            customer=self.customer,
            seller=self.seller,
            transaction_id='123456789012',
            is_full_cash=True,
            group_discount=self.group_discount
        )
        OrderItem.objects.create(
            order=order,
            inventory=self.inventory,
            price=self.inventory.SKU.price
        )
        self.inventory.status = 'sold'
        self.inventory.save()
        self.group_discount.used_count = 1
        self.group_discount.save()

        url = reverse('order-detail', args=[order.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # بررسی وضعیت موجودی
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.status, 'available')
        
        # بررسی به‌روزرسانی تخفیف گروهی
        self.group_discount.refresh_from_db()
        self.assertEqual(self.group_discount.used_count, 0)
