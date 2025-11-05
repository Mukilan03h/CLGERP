from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyViewSet, LeaveRequestViewSet

router = DefaultRouter()
router.register(r'faculty', FacultyViewSet)
router.register(r'leave-requests', LeaveRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
