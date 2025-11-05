from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LedgerViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'ledgers', LedgerViewSet)
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
