from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApplicationViewSet, AdmissionViewSet

router = DefaultRouter()
router.register(r'applications', ApplicationViewSet, basename='admission-application')
router.register(r'admissions', AdmissionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
