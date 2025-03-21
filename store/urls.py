from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProvinceViewSet, CityViewSet, CompanyViewSet, StoreViewSet

router = DefaultRouter()
router.register(r'provinces', ProvinceViewSet)
router.register(r'cities', CityViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'stores', StoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 