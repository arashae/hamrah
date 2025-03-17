from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Province, City, Company, Store
from .serializers import ProvinceSerializer, CitySerializer, CompanySerializer, StoreSerializer
from accounts.permissions import IsAdmin

# Create your views here.

class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = City.objects.all()
        province = self.request.query_params.get('province', None)
        if province is not None:
            queryset = queryset.filter(province_id=province)
        return queryset

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Store.objects.all()
        city = self.request.query_params.get('city', None)
        company = self.request.query_params.get('company', None)
        is_active = self.request.query_params.get('is_active', None)

        if city is not None:
            queryset = queryset.filter(city_id=city)
        if company is not None:
            queryset = queryset.filter(company_id=company)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
