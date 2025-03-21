from django.urls import path
from . import views

urlpatterns = [
    # مدیریت استان‌ها و شهرها
    path('provinces/', views.manage_provinces, name='manage-provinces'),
    path('cities/', views.manage_cities, name='manage-cities'),
    
    # مدیریت شرکت‌ها و فروشگاه‌ها
    path('companies/define/', views.define_company, name='define-company'),
    path('stores/define/', views.define_store, name='define-store'),
    path('stores/<int:store_id>/toggle-status/', views.toggle_store_status, name='toggle-store-status'),
    path('stores/search/', views.search_stores, name='search-stores'),
    
    # مدیریت برندها و انواع دستگاه‌ها
    path('brands/define/', views.define_brand, name='define-brand'),
    path('types/define/', views.define_type, name='define-type'),
    path('portions/define/', views.define_portion_plan, name='define-portion'),
    
    # مدیریت دستگاه‌ها
    path('devices/define/', views.define_device, name='define-device'),
    path('devices/<int:device_id>/toggle-status/', views.toggle_device_status, name='toggle-device-status'),
    path('devices/search/', views.search_devices, name='search-devices'),
    
    # مدیریت ادمین‌ها
    path('admins/define/', views.define_admin, name='define-admin'),
    
    # مدیریت تامین‌کنندگان
    path('suppliers/define/', views.define_supplier, name='define-supplier'),
    path('suppliers/<int:supplier_id>/toggle-status/', views.toggle_supplier_status, name='toggle-supplier-status'),
    path('suppliers/search/', views.search_suppliers, name='search-suppliers'),
] 