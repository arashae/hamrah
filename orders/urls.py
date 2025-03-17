from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (IndividualDiscountViewSet, GroupDiscountViewSet, LoanViewSet,
                   OrderViewSet, OrderItemViewSet)

router = DefaultRouter()
router.register(r'individual-discounts', IndividualDiscountViewSet)
router.register(r'group-discounts', GroupDiscountViewSet)
router.register(r'loans', LoanViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 