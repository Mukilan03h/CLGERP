from django.urls import path
from .views import (
    SubjectListCreateView,
    SubjectRetrieveUpdateDestroyAPIView,
    AttendanceListCreateView,
    AttendanceRetrieveUpdateDestroyAPIView,
    StudentAttendanceView,
    AttendanceReportView,
)

urlpatterns = [
    path('subjects/', SubjectListCreateView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyAPIView.as_view(), name='subject-retrieve-update-destroy'),
    path('mark/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('<int:pk>/', AttendanceRetrieveUpdateDestroyAPIView.as_view(), name='attendance-retrieve-update-destroy'),
    path('student/<int:student_id>/', StudentAttendanceView.as_view(), name='student-attendance'),
    path('report/<int:semester>/', AttendanceReportView.as_view(), name='attendance-report'),
]
