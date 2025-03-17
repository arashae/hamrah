from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Admin, Customer, Seller

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