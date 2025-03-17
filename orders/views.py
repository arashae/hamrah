from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
import logging
from .models import IndividualDiscount, GroupDiscount, Loan, Order, OrderItem
from .serializers import (IndividualDiscountSerializer, GroupDiscountSerializer,
                        LoanSerializer, OrderSerializer, OrderItemSerializer)
from accounts.permissions import IsAdmin, IsSeller
from inventory.models import Inventory

# تنظیم لاگر
logger = logging.getLogger('orders')

class IndividualDiscountViewSet(viewsets.ModelViewSet):
    queryset = IndividualDiscount.objects.all()
    serializer_class = IndividualDiscountSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = IndividualDiscount.objects.all()
        customer = self.request.query_params.get('customer', None)
        active = self.request.query_params.get('active', None)

        if customer is not None:
            queryset = queryset.filter(customer_id=customer)
        if active is not None and active.lower() == 'true':
            queryset = queryset.filter(active_date__gte=timezone.now())
        
        return queryset

class GroupDiscountViewSet(viewsets.ModelViewSet):
    queryset = GroupDiscount.objects.all()
    serializer_class = GroupDiscountSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = GroupDiscount.objects.all()
        available = self.request.query_params.get('available', None)

        if available is not None and available.lower() == 'true':
            queryset = queryset.filter(used_count__lt=models.F('max_use'))
        
        return queryset

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdmin|IsSeller]

    def get_queryset(self):
        queryset = Order.objects.all()
        
        # اگر کاربر فروشنده است، فقط سفارشات خودش را ببیند
        if hasattr(self.request.user, 'seller'):
            queryset = queryset.filter(seller=self.request.user.seller)
        
        customer = self.request.query_params.get('customer', None)
        seller = self.request.query_params.get('seller', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        is_full_cash = self.request.query_params.get('is_full_cash', None)

        if customer is not None:
            queryset = queryset.filter(customer_id=customer)
        if seller is not None:
            queryset = queryset.filter(seller_id=seller)
        if start_date is not None:
            queryset = queryset.filter(order_date__gte=start_date)
        if end_date is not None:
            queryset = queryset.filter(order_date__lte=end_date)
        if is_full_cash is not None:
            queryset = queryset.filter(is_full_cash=is_full_cash.lower() == 'true')
        
        return queryset

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            # اگر کاربر فروشنده است، خودش را به عنوان فروشنده ثبت کند
            if hasattr(request.user, 'seller'):
                request.data['seller'] = request.user.seller.id

            # بررسی موجودی محصولات
            items_data = request.data.pop('items', [])
            for item in items_data:
                inventory = Inventory.objects.get(id=item['inventory'])
                if inventory.status != 'available':
                    logger.error(f'محصول با شناسه {inventory.id} در دسترس نیست')
                    return Response(
                        {'error': f'محصول با شناسه {inventory.id} در دسترس نیست'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # ایجاد سفارش
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()
            logger.info(f'سفارش جدید با شناسه {order.id} ایجاد شد')

            # ایجاد آیتم‌های سفارش
            total_price = 0
            for item in items_data:
                item['order'] = order.id
                inventory = Inventory.objects.get(id=item['inventory'])
                item['price'] = inventory.SKU.price
                if not item.get('price'):
                    item['price'] = inventory.SKU.price
                total_price += item['price']
                
                item_serializer = OrderItemSerializer(data=item)
                item_serializer.is_valid(raise_exception=True)
                item_serializer.save()

                # به‌روزرسانی وضعیت موجودی
                inventory.status = 'sold'
                inventory.save()
                logger.info(f'موجودی با شناسه {inventory.id} به وضعیت فروش رفته تغییر کرد')

            # به‌روزرسانی تخفیف گروهی
            if order.group_discount:
                order.group_discount.used_count += 1
                order.group_discount.save()
                logger.info(f'تخفیف گروهی با شناسه {order.group_discount.id} به‌روزرسانی شد')

            logger.info(f'سفارش با شناسه {order.id} با موفقیت ثبت شد. مبلغ کل: {total_price}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f'خطا در ثبت سفارش: {str(e)}')
            return Response(
                {'error': 'خطا در ثبت سفارش'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # برگرداندن وضعیت موجودی‌ها به حالت قبل
            for item in instance.orderitem_set.all():
                inventory = item.inventory
                inventory.status = 'available'
                inventory.save()
                logger.info(f'موجودی با شناسه {inventory.id} به وضعیت موجود تغییر کرد')

            # به‌روزرسانی تخفیف گروهی
            if instance.group_discount:
                instance.group_discount.used_count -= 1
                instance.group_discount.save()
                logger.info(f'تخفیف گروهی با شناسه {instance.group_discount.id} به‌روزرسانی شد')

            logger.info(f'سفارش با شناسه {instance.id} حذف شد')
            return super().destroy(request, *args, **kwargs)

        except Exception as e:
            logger.error(f'خطا در حذف سفارش: {str(e)}')
            return Response(
                {'error': 'خطا در حذف سفارش'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAdmin|IsSeller]

    def get_queryset(self):
        queryset = OrderItem.objects.all()
        
        # اگر کاربر فروشنده است، فقط آیتم‌های سفارشات خودش را ببیند
        if hasattr(self.request.user, 'seller'):
            queryset = queryset.filter(order__seller=self.request.user.seller)
        
        order = self.request.query_params.get('order', None)
        inventory = self.request.query_params.get('inventory', None)

        if order is not None:
            queryset = queryset.filter(order_id=order)
        if inventory is not None:
            queryset = queryset.filter(inventory_id=inventory)
        
        return queryset
