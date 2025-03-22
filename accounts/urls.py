from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    # URLs مربوط به احراز هویت
    path('token/', views.obtain_token, name='token_obtain'),
    path('token/refresh/', views.refresh_token, name='token_refresh'),
    
    # URLs مدیریت کاربران توسط سوپر ادمین
    path('store-admins/', views.store_admin_list, name='store-admin-list'),
    path('store-admins/create/', views.create_store_admin, name='create-store-admin'),
    path('store-admins/<int:admin_id>/toggle-status/', views.toggle_store_admin_status, name='toggle-store-admin-status'),
    
    # URLs مدیریت کاربران توسط ادمین فروشگاه
    path('store-users/', views.store_user_list, name='store-user-list'),
    path('store-users/create/', views.create_store_user, name='create-store-user'),
    path('store-users/<int:user_id>/toggle-status/', views.toggle_store_user_status, name='toggle-store-user-status'),

    # URLs پروفایل کاربر
    path('profile/', views.user_profile, name='user-profile'),
    path('change-password/', views.change_password, name='change-password'),

    # URLs مربوط به مشتریان
    path('', include(router.urls)),
] 