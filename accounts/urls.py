from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminViewSet, CustomerViewSet, SellerViewSet

router = DefaultRouter()
router.register(r'admins', AdminViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'sellers', SellerViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 