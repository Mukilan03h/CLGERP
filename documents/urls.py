from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, CertificateViewSet

router = DefaultRouter()
router.register(r'user-documents', DocumentViewSet)
router.register(r'certificates', CertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
