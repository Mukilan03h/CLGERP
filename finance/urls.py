from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeeStructureViewSet, FeePaymentViewSet, ExpenseViewSet

router = DefaultRouter()
router.register(r'fee-structures', FeeStructureViewSet)
router.register(r'fee-payments', FeePaymentViewSet)
router.register(r'expenses', ExpenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
