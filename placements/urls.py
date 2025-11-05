from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, JobViewSet, ApplicationViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
