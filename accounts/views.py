from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Admin, Customer, Seller, User
from .serializers import AdminSerializer, CustomerSerializer, SellerSerializer, UserSerializer, StoreUserSerializer, StoreAdminSerializer
from .permissions import IsAdmin, IsSeller, IsCustomer, IsOwnerOrAdmin
from .auth import authenticate_admin, authenticate_seller, get_tokens_for_user
import logging

logger = logging.getLogger('accounts')

# Create your views here.

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        admin = authenticate_admin(username, password)
        if admin:
            tokens = get_tokens_for_user(admin, 'admin')
            return Response({
                'user': self.get_serializer(admin).data,
                'tokens': tokens
            })
        return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdmin|IsCustomer]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAdmin|IsSeller]

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        seller = authenticate_seller(username, password)
        if seller:
            tokens = get_tokens_for_user(seller, 'seller')
            return Response({
                'user': self.get_serializer(seller).data,
                'tokens': tokens
            })
        return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'}, 
                      status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def obtain_token(request):
    """دریافت توکن با نام کاربری و رمز عبور"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        logger.info(f'User {username} logged in successfully')
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })
    logger.warning(f'Failed login attempt for username {username}')
    return Response({'error': 'نام کاربری یا رمز عبور اشتباه است'}, 
                  status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def refresh_token(request):
    """تمدید توکن با استفاده از refresh token"""
    try:
        refresh = RefreshToken(request.data.get('refresh'))
        return Response({
            'access': str(refresh.access_token)
        })
    except Exception as e:
        logger.error(f'Token refresh failed: {str(e)}')
        return Response({'error': 'توکن نامعتبر است'}, 
                      status=status.HTTP_400_BAD_REQUEST)

class IsSuperAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.role == 'superadmin'

class IsStoreAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.role == 'store_admin'

@api_view(['POST'])
@permission_classes([IsSuperAdmin])
def create_store_admin(request):
    """ایجاد ادمین فروشگاه توسط سوپر ادمین"""
    serializer = StoreAdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        logger.info(f'Store admin {admin.username} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsStoreAdmin])
def create_store_user(request):
    """ایجاد فروشنده یا انباردار توسط ادمین فروشگاه"""
    serializer = StoreUserSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        logger.info(f'{user.get_role_display()} {user.username} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsStoreAdmin])
def list_store_users(request):
    """لیست کاربران یک فروشگاه"""
    users = User.objects.filter(store=request.user.store)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsStoreAdmin])
def toggle_user_status(request, user_id):
    """فعال/غیرفعال کردن کاربر فروشگاه"""
    try:
        user = User.objects.get(id=user_id, store=request.user.store)
        user.is_active = not user.is_active
        user.save()
        logger.info(f'User {user.username} {"activated" if user.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': user.is_active})
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def list_store_admins(request):
    """لیست ادمین‌های فروشگاه‌ها"""
    admins = User.objects.filter(role='store_admin')
    serializer = UserSerializer(admins, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsSuperAdmin])
def toggle_admin_status(request, admin_id):
    """فعال/غیرفعال کردن ادمین فروشگاه"""
    try:
        admin = User.objects.get(id=admin_id, role='store_admin')
        admin.is_active = not admin.is_active
        admin.save()
        logger.info(f'Store admin {admin.username} {"activated" if admin.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': admin.is_active})
    except User.DoesNotExist:
        return Response({'error': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
