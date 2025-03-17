from rest_framework import serializers
from .models import Brand, Category, Device, Supplier, Guarantee, PortionPlan, SKU, Inventory

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'brand']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']

class DeviceSerializer(serializers.ModelSerializer):
    brand_detail = BrandSerializer(source='brand', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Device
        fields = ['id', 'category', 'category_detail', 'brand', 'brand_detail',
                 'model', 'RAM', 'storage', 'color', 'pack', 'network', 'is_active']
        extra_kwargs = {
            'category': {'write_only': True},
            'brand': {'write_only': True},
        }

class SupplierSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Supplier
        fields = ['id', 'username', 'password', 'name', 'phone_number', 'is_active']

    def create(self, validated_data):
        if 'password' in validated_data:
            from django.contrib.auth.hashers import make_password
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = ['id', 'guarantee']

class PortionPlanSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = PortionPlan
        fields = ['id', 'category', 'category_detail', 'MCI_portion', 
                 'store_portion', 'supplier_portion']
        extra_kwargs = {
            'category': {'write_only': True},
        }

class SKUSerializer(serializers.ModelSerializer):
    device_detail = DeviceSerializer(source='device', read_only=True)
    supplier_detail = SupplierSerializer(source='supplier', read_only=True)
    guarantee_detail = GuaranteeSerializer(source='guarantee', read_only=True)

    class Meta:
        model = SKU
        fields = ['id', 'device', 'device_detail', 'supplier', 'supplier_detail',
                 'price', 'guarantee', 'guarantee_detail', 'timestamp', 'detail']
        extra_kwargs = {
            'device': {'write_only': True},
            'supplier': {'write_only': True},
            'guarantee': {'write_only': True},
        }

class InventorySerializer(serializers.ModelSerializer):
    store_detail = serializers.SerializerMethodField()
    SKU_detail = SKUSerializer(source='SKU', read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'store', 'store_detail', 'SKU', 'SKU_detail', 'IMEI',
                 'receive_date', 'submission_date', 'discount_rate', 'status']
        extra_kwargs = {
            'store': {'write_only': True},
            'SKU': {'write_only': True},
        }

    def get_store_detail(self, obj):
        from store.serializers import StoreSerializer
        return StoreSerializer(obj.store).data 