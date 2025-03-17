from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Brand, Category, Device, Supplier, Guarantee, PortionPlan, SKU, Inventory
from .serializers import (BrandSerializer, CategorySerializer, DeviceSerializer,
                        SupplierSerializer, GuaranteeSerializer, PortionPlanSerializer,
                        SKUSerializer, InventorySerializer)
from accounts.permissions import IsAdmin, IsSeller

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Device.objects.all()
        category = self.request.query_params.get('category', None)
        brand = self.request.query_params.get('brand', None)
        is_active = self.request.query_params.get('is_active', None)

        if category is not None:
            queryset = queryset.filter(category_id=category)
        if brand is not None:
            queryset = queryset.filter(brand_id=brand)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        from accounts.auth import authenticate_supplier, get_tokens_for_user
        supplier = authenticate_supplier(username, password)
        if supplier:
            tokens = get_tokens_for_user(supplier, 'supplier')
            return Response({
                'user': self.get_serializer(supplier).data,
                'tokens': tokens
            })
        return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class GuaranteeViewSet(viewsets.ModelViewSet):
    queryset = Guarantee.objects.all()
    serializer_class = GuaranteeSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class PortionPlanViewSet(viewsets.ModelViewSet):
    queryset = PortionPlan.objects.all()
    serializer_class = PortionPlanSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class SKUViewSet(viewsets.ModelViewSet):
    queryset = SKU.objects.all()
    serializer_class = SKUSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = SKU.objects.all()
        device = self.request.query_params.get('device', None)
        supplier = self.request.query_params.get('supplier', None)
        guarantee = self.request.query_params.get('guarantee', None)

        if device is not None:
            queryset = queryset.filter(device_id=device)
        if supplier is not None:
            queryset = queryset.filter(supplier_id=supplier)
        if guarantee is not None:
            queryset = queryset.filter(guarantee_id=guarantee)
        
        return queryset

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAdmin|IsSeller]

    def get_queryset(self):
        queryset = Inventory.objects.all()
        
        # اگر کاربر فروشنده است، فقط موجودی فروشگاه خودش را ببیند
        if hasattr(self.request.user, 'seller'):
            queryset = queryset.filter(store=self.request.user.seller.store)
        
        store = self.request.query_params.get('store', None)
        sku = self.request.query_params.get('sku', None)
        status = self.request.query_params.get('status', None)
        imei = self.request.query_params.get('imei', None)

        if store is not None:
            queryset = queryset.filter(store_id=store)
        if sku is not None:
            queryset = queryset.filter(SKU_id=sku)
        if status is not None:
            queryset = queryset.filter(status=status)
        if imei is not None:
            queryset = queryset.filter(IMEI__icontains=imei)
        
        return queryset
