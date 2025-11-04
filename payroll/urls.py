from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaryViewSet, PayslipViewSet, PayslipEntryViewSet

router = DefaultRouter()
router.register(r'salaries', SalaryViewSet)
router.register(r'payslips', PayslipViewSet)
router.register(r'payslip-entries', PayslipEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
