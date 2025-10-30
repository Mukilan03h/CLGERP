from django.urls import path
from .views import StudentListCreateView, StudentRetrieveUpdateDestroyAPIView, StudentByRollNoView

urlpatterns = [
    path('', StudentListCreateView.as_view(), name='student-list-create'),
    path('<int:pk>/', StudentRetrieveUpdateDestroyAPIView.as_view(), name='student-retrieve-update-destroy'),
    path('roll/<str:roll_no>/', StudentByRollNoView.as_view(), name='student-by-roll-no'),
]
