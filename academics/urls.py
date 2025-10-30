from django.urls import path
from .views import (
    ProgramListCreateView,
    ProgramRetrieveUpdateDestroyAPIView,
    CourseListCreateView,
    CourseRetrieveUpdateDestroyAPIView,
    SyllabusListCreateView,
    SyllabusRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('programs/', ProgramListCreateView.as_view(), name='program-list-create'),
    path('programs/<int:pk>/', ProgramRetrieveUpdateDestroyAPIView.as_view(), name='program-retrieve-update-destroy'),
    path('courses/', CourseListCreateView.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-retrieve-update-destroy'),
    path('syllabi/', SyllabusListCreateView.as_view(), name='syllabus-list-create'),
    path('syllabi/<int:pk>/', SyllabusRetrieveUpdateDestroyAPIView.as_view(), name='syllabus-retrieve-update-destroy'),
]
