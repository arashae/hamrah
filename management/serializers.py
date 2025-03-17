from rest_framework import serializers
from .models import (
    Admin, Company, Province, City, Store, Brand,
    Category, PortionPlan, Device, Supplier
)

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = ('id', 'username', 'password', 'name', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        admin = Admin(**validated_data)
        admin.set_password(password)
        admin.save()
        return admin

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ('id', 'province')

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'city', 'province')

class StoreSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    city = CitySerializer(read_only=True)
    city_id = serializers.IntegerField(write_only=True)
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Store
        fields = ('id', 'username', 'password', 'name', 'city', 'city_id',
                 'type', 'company', 'company_id', 'manager', 'phone_number',
                 'address', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'brand')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category')

class PortionPlanSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = PortionPlan
        fields = ('id', 'category', 'category_id', 'MCI_portion',
                 'store_portion', 'supplier_portion')

class DeviceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Device
        fields = ('id', 'category', 'category_id', 'brand', 'brand_id',
                 'model', 'RAM', 'storage', 'color', 'pack', 'network',
                 'is_active')

class SupplierSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Supplier
        fields = ('id', 'username', 'password', 'name', 'phone_number',
                 'is_active')
        extra_kwargs = {'password': {'write_only': True}} 