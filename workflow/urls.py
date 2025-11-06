from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet, StageViewSet, TransitionViewSet

router = DefaultRouter()
router.register(r'workflows', WorkflowViewSet)
router.register(r'stages', StageViewSet)
router.register(r'transitions', TransitionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
