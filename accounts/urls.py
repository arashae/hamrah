from django.urls import path
from . import views

urlpatterns = [
    # URLs مربوط به احراز هویت
    path('token/', views.obtain_token, name='token_obtain'),
    path('token/refresh/', views.refresh_token, name='token_refresh'),
    
    # URLs مدیریت کاربران توسط سوپر ادمین
    path('store-admin/create/', views.create_store_admin, name='create-store-admin'),
    path('store-admin/list/', views.list_store_admins, name='list-store-admins'),
    path('store-admin/<int:admin_id>/toggle-status/', views.toggle_admin_status, name='toggle-admin-status'),
    
    # URLs مدیریت کاربران توسط ادمین فروشگاه
    path('store-user/create/', views.create_store_user, name='create-store-user'),
    path('store-user/list/', views.list_store_users, name='list-store-users'),
    path('store-user/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle-user-status'),
] 