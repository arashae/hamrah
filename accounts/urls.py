from django.urls import path
from . import views

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
] 