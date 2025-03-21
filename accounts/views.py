from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, StoreUserSerializer, StoreAdminSerializer
from .permissions import IsAdmin, IsSeller
import logging

logger = logging.getLogger('accounts')

class IsSuperAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.role == 'superadmin'

class IsStoreAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.role == 'store_admin'

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def obtain_token(request):
    """دریافت توکن با استفاده از نام کاربری و رمز عبور"""
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        refresh = RefreshToken.for_user(user)
        logger.info(f'User {username} logged in successfully')
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'full_name': user.full_name,
                'role': user.role,
                'role_display': user.get_role_display(),
                'store': user.store.id if user.store else None,
                'store_name': user.store.name if user.store else None
            }
        })
    logger.warning(f'Failed login attempt for username {username}')
    return Response({'error': 'Invalid credentials or user is inactive'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def refresh_token(request):
    """تازه کردن توکن با استفاده از refresh token"""
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        return Response({
            'access': str(token.access_token),
        })
    except Exception as e:
        logger.error(f'Token refresh failed: {str(e)}')
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def store_admin_list(request):
    """لیست ادمین‌های فروشگاه"""
    admins = User.objects.filter(role='store_admin')
    serializer = StoreAdminSerializer(admins, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsSuperAdmin])
def create_store_admin(request):
    """ایجاد ادمین فروشگاه جدید"""
    serializer = StoreAdminSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        logger.info(f'Store admin {admin.username} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsSuperAdmin])
def toggle_store_admin_status(request, admin_id):
    """فعال/غیرفعال کردن ادمین فروشگاه"""
    try:
        admin = User.objects.get(id=admin_id, role='store_admin')
        admin.is_active = not admin.is_active
        admin.save()
        logger.info(f'Store admin {admin.username} {"activated" if admin.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': admin.is_active})
    except User.DoesNotExist:
        return Response({'error': 'Store admin not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsStoreAdmin])
def store_user_list(request):
    """لیست کاربران فروشگاه"""
    users = User.objects.filter(store=request.user.store)
    serializer = StoreUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsStoreAdmin])
def create_store_user(request):
    """ایجاد کاربر فروشگاه جدید"""
    data = request.data.copy()
    data['store'] = request.user.store.id
    serializer = StoreUserSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        logger.info(f'Store user {user.username} created by {request.user.username}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsStoreAdmin])
def toggle_store_user_status(request, user_id):
    """فعال/غیرفعال کردن کاربر فروشگاه"""
    try:
        user = User.objects.get(id=user_id, store=request.user.store)
        user.is_active = not user.is_active
        user.save()
        logger.info(f'Store user {user.username} {"activated" if user.is_active else "deactivated"} by {request.user.username}')
        return Response({'status': 'success', 'is_active': user.is_active})
    except User.DoesNotExist:
        return Response({'error': 'Store user not found'}, status=status.HTTP_404_NOT_FOUND)
