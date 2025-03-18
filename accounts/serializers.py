from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Admin, Customer, Seller, User
from management.models import Store

class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Admin
        fields = ['id', 'username', 'password', 'name', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'national_code', 'phone_number', 
                 'gender', 'id_card', 'address', 'postal_code']

class SellerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Seller
        fields = ['id', 'username', 'password', 'name', 'store']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'phone', 
                 'national_code', 'role', 'role_display', 'store', 'store_name', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'store': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class StoreUserSerializer(serializers.ModelSerializer):
    """سریالایزر برای ایجاد کاربران فروشگاه (فروشنده و انباردار)"""
    password = serializers.CharField(write_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'phone', 
                 'national_code', 'role', 'role_display', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_role(self, value):
        if value not in ['seller', 'warehouse']:
            raise serializers.ValidationError(
                "نقش کاربر باید فروشنده یا انباردار باشد"
            )
        return value

    def create(self, validated_data):
        # اضافه کردن فروشگاه به داده‌های کاربر
        request = self.context.get('request')
        if request and hasattr(request.user, 'store'):
            validated_data['store'] = request.user.store
        
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class StoreAdminSerializer(serializers.ModelSerializer):
    """سریالایزر برای ایجاد ادمین فروشگاه"""
    password = serializers.CharField(write_only=True)
    store = serializers.PrimaryKeyRelatedField(queryset=Store.objects.all())
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'phone', 
                 'national_code', 'store', 'role_display', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'store_admin'
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user 