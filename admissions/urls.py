from django.urls import path
from .views import (
    ApplicationFormListCreateView,
    ApplicationFormRetrieveUpdateDestroyAPIView,
    ApplicationStatusView,
    VerifyApplicationView,
    MeritListListCreateView,
    MeritListRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path('apply/', ApplicationFormListCreateView.as_view(), name='application-form-list-create'),
    path('<int:pk>/', ApplicationFormRetrieveUpdateDestroyAPIView.as_view(), name='application-form-retrieve-update-destroy'),
    path('status/<int:pk>/', ApplicationStatusView.as_view(), name='application-status'),
    path('verify/<int:pk>/', VerifyApplicationView.as_view(), name='verify-application'),
    path('merit-list/', MeritListListCreateView.as_view(), name='merit-list-list-create'),
    path('merit-list/<int:pk>/', MeritListRetrieveUpdateDestroyAPIView.as_view(), name='merit-list-retrieve-update-destroy'),
]
