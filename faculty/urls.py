from django.urls import path
from .views import (
    FacultyListCreateView,
    FacultyRetrieveUpdateDestroyAPIView,
    LeaveRequestListCreateView,
    LeaveRequestRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('', FacultyListCreateView.as_view(), name='faculty-list-create'),
    path('<int:pk>/', FacultyRetrieveUpdateDestroyAPIView.as_view(), name='faculty-retrieve-update-destroy'),
    path('leave-requests/', LeaveRequestListCreateView.as_view(), name='leave-request-list-create'),
    path('leave-requests/<int:pk>/', LeaveRequestRetrieveUpdateDestroyAPIView.as_view(), name='leave-request-retrieve-update-destroy'),
]
