from django.urls import path
from . import views

urlpatterns = [
    path('provinces/', views.manage_provinces, name='manage-provinces'),
    path('cities/', views.manage_cities, name='manage-cities'),
    path('define-company/', views.define_company, name='define-company'),
    path('define-store/', views.define_store, name='define-store'),
    path('define-brand/', views.define_brand, name='define-brand'),
    path('define-type/', views.define_type, name='define-type'),
    path('define-portion-plan/', views.define_portion_plan, name='define-portion-plan'),
    path('define-device/', views.define_device, name='define-device'),
    path('define-admin/', views.define_admin, name='define-admin'),
    path('define-supplier/', views.define_supplier, name='define-supplier'),
    path('store/<int:store_id>/toggle-status/', views.toggle_store_status, name='toggle-store-status'),
    path('device/<int:device_id>/toggle-status/', views.toggle_device_status, name='toggle-device-status'),
    path('supplier/<int:supplier_id>/toggle-status/', views.toggle_supplier_status, name='toggle-supplier-status'),
    path('search/stores/', views.search_stores, name='search-stores'),
    path('search/devices/', views.search_devices, name='search-devices'),
    path('search/suppliers/', views.search_suppliers, name='search-suppliers'),
] 