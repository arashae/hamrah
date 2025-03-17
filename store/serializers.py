from rest_framework import serializers
from .models import Province, City, Company, Store

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'province']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city', 'province']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name']

class StoreSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    city_detail = CitySerializer(source='city', read_only=True)
    company_detail = CompanySerializer(source='company', read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'username', 'password', 'name', 'city', 'city_detail',
                 'type', 'company', 'company_detail', 'manager', 'phone_number',
                 'address', 'is_active']
        extra_kwargs = {
            'city': {'write_only': True},
            'company': {'write_only': True},
        }

    def create(self, validated_data):
        if 'password' in validated_data:
            from django.contrib.auth.hashers import make_password
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data) 