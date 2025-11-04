from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClassroomViewSet, TimeSlotViewSet, TimetableViewSet

router = DefaultRouter()
router.register(r'classrooms', ClassroomViewSet)
router.register(r'timeslots', TimeSlotViewSet)
router.register(r'timetables', TimetableViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
