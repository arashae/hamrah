from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    Admin, Company, Province, City, Store, Brand,
    Category, PortionPlan, Device, Supplier
)
from .serializers import (
    AdminSerializer, CompanySerializer, ProvinceSerializer,
    CitySerializer, StoreSerializer, BrandSerializer,
    CategorySerializer, PortionPlanSerializer,
    DeviceSerializer, SupplierSerializer
)
import logging

logger = logging.getLogger('management')

class IsAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.role == 'admin'

@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def manage_provinces(request):
    """مدیریت استان‌ها"""
    if request.method == 'GET':
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ProvinceSerializer(data=request.data)
        if serializer.is_valid():
            province = serializer.save()
            logger.info(f'Province {province.province} created by {request.user.username}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAdmin])
def manage_cities(request):
    """مدیریت شهرها"""
    if request.method == 'GET':
        province_id = request.query_params.get('province_id')
        if province_id:
            cities = City.objects.filter(province_id=province_id)
        else:
            cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.save()
            logger.info(f'City {city.city} created by {request.user.username}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_company(request):
    """تعریف شرکت جدید"""
    serializer = CompanySerializer(data=request.data)
    if serializer.is_valid():
        company = serializer.save()
        logger.info(f'Company {company.name} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_store(request):
    """تعریف فروشگاه جدید"""
    serializer = StoreSerializer(data=request.data)
    if serializer.is_valid():
        store = serializer.save()
        logger.info(f'Store {store.name} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_brand(request):
    """تعریف برند جدید"""
    serializer = BrandSerializer(data=request.data)
    if serializer.is_valid():
        brand = serializer.save()
        logger.info(f'Brand {brand.brand} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_type(request):
    """تعریف نوع دستگاه جدید"""
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        category = serializer.save()
        logger.info(f'Category {category.category} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_portion_plan(request):
    """تعریف طرح سهم‌بندی جدید"""
    serializer = PortionPlanSerializer(data=request.data)
    if serializer.is_valid():
        plan = serializer.save()
        logger.info(f'Portion plan for category {plan.category.category} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_device(request):
    """تعریف دستگاه جدید"""
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        device = serializer.save()
        logger.info(f'Device {device.model} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_admin(request):
    """تعریف ادمین جدید"""
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        logger.info(f'Admin {admin.username} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def define_supplier(request):
    """تعریف تامین‌کننده جدید"""
    serializer = SupplierSerializer(data=request.data)
    if serializer.is_valid():
        supplier = serializer.save()
        logger.info(f'Supplier {supplier.name} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdmin])
def toggle_store_status(request, store_id):
    """فعال/غیرفعال کردن فروشگاه"""
    try:
        store = Store.objects.get(id=store_id)
        store.is_active = not store.is_active
        store.save()
        logger.info(f'Store {store.name} {"activated" if store.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': store.is_active})
    except Store.DoesNotExist:
        return Response({'error': 'Store not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdmin])
def toggle_device_status(request, device_id):
    """فعال/غیرفعال کردن دستگاه"""
    try:
        device = Device.objects.get(id=device_id)
        device.is_active = not device.is_active
        device.save()
        logger.info(f'Device {device.model} {"activated" if device.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': device.is_active})
    except Device.DoesNotExist:
        return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAdmin])
def toggle_supplier_status(request, supplier_id):
    """فعال/غیرفعال کردن تامین‌کننده"""
    try:
        supplier = Supplier.objects.get(id=supplier_id)
        supplier.is_active = not supplier.is_active
        supplier.save()
        logger.info(f'Supplier {supplier.name} {"activated" if supplier.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': supplier.is_active})
    except Supplier.DoesNotExist:
        return Response({'error': 'Supplier not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdmin])
def search_stores(request):
    """جستجو در فروشگاه‌ها"""
    name = request.query_params.get('name', '')
    city_id = request.query_params.get('city_id')
    company_id = request.query_params.get('company_id')
    is_active = request.query_params.get('is_active')

    stores = Store.objects.all()
    if name:
        stores = stores.filter(name__icontains=name)
    if city_id:
        stores = stores.filter(city_id=city_id)
    if company_id:
        stores = stores.filter(company_id=company_id)
    if is_active is not None:
        stores = stores.filter(is_active=is_active.lower() == 'true')

    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdmin])
def search_devices(request):
    """جستجو در دستگاه‌ها"""
    model = request.query_params.get('model', '')
    category_id = request.query_params.get('category_id')
    brand_id = request.query_params.get('brand_id')
    is_active = request.query_params.get('is_active')

    devices = Device.objects.all()
    if model:
        devices = devices.filter(model__icontains=model)
    if category_id:
        devices = devices.filter(category_id=category_id)
    if brand_id:
        devices = devices.filter(brand_id=brand_id)
    if is_active is not None:
        devices = devices.filter(is_active=is_active.lower() == 'true')

    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdmin])
def search_suppliers(request):
    """جستجو در تامین‌کنندگان"""
    name = request.query_params.get('name', '')
    is_active = request.query_params.get('is_active')

    suppliers = Supplier.objects.all()
    if name:
        suppliers = suppliers.filter(name__icontains=name)
    if is_active is not None:
        suppliers = suppliers.filter(is_active=is_active.lower() == 'true')

    serializer = SupplierSerializer(suppliers, many=True)
    return Response(serializer.data) 