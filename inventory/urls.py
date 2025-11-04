from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, AssetViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet)
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
