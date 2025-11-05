from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
