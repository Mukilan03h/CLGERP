from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HostelViewSet, RoomViewSet, AllocationViewSet

router = DefaultRouter()
router.register(r'hostels', HostelViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'allocations', AllocationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
