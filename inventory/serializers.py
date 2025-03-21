from rest_framework import serializers
from .models import (Brand, Category, Device, Supplier, Guarantee,
                    PortionPlan, SKU, Inventory)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']

class DeviceSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.brand', read_only=True)
    category_name = serializers.CharField(source='category.category', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'category', 'category_name', 'brand', 'brand_name',
                 'model', 'RAM', 'storage', 'color', 'pack', 'network', 'is_active']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'username', 'password', 'name', 'phone_number', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = ['id', 'guarantee']

class PortionPlanSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.category', read_only=True)

    class Meta:
        model = PortionPlan
        fields = ['id', 'category', 'category_name', 'MCI_portion',
                 'store_portion', 'supplier_portion']

class SKUSerializer(serializers.ModelSerializer):
    device_detail = DeviceSerializer(source='device', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    guarantee_name = serializers.CharField(source='guarantee.guarantee', read_only=True)

    class Meta:
        model = SKU
        fields = ['id', 'device', 'device_detail', 'supplier', 'supplier_name',
                 'price', 'guarantee', 'guarantee_name', 'timestamp', 'detail']

class InventorySerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)
    sku_detail = SKUSerializer(source='SKU', read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'store', 'store_name', 'SKU', 'sku_detail', 'IMEI',
                 'receive_date', 'submission_date', 'discount_rate', 'status'] 