from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookIssueViewSet, FineViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'book-issues', BookIssueViewSet)
router.register(r'fines', FineViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
