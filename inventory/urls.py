from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (BrandViewSet, CategoryViewSet, DeviceViewSet, SupplierViewSet,
                   GuaranteeViewSet, PortionPlanViewSet, SKUViewSet, InventoryViewSet)

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'devices', DeviceViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'guarantees', GuaranteeViewSet)
router.register(r'portion-plans', PortionPlanViewSet)
router.register(r'skus', SKUViewSet)
router.register(r'inventories', InventoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 