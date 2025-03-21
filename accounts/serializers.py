from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Customer

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'full_name', 'phone', 'national_code', 
                 'role', 'role_display', 'store', 'store_name', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'store': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class StoreUserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'phone', 'national_code', 'role', 'role_display', 'store', 'store_name', 'is_active')
        read_only_fields = ('id', 'role_display', 'store_name', 'is_active', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'seller'
        user = User.objects.create_user(**validated_data)
        return user

class StoreAdminSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'full_name', 'phone', 'national_code', 'role', 'role_display', 'store', 'store_name', 'is_active')
        read_only_fields = ('id', 'role_display', 'store_name', 'is_active', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['role'] = 'store_admin'
        user = User.objects.create_user(**validated_data)
        return user

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'national_code', 'phone_number', 
                 'gender', 'id_card', 'address', 'postal_code'] 