from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExamViewSet, MarksViewSet, ResultViewSet

router = DefaultRouter()
router.register(r'exams', ExamViewSet)
router.register(r'marks', MarksViewSet)
router.register(r'results', ResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
