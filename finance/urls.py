from django.urls import path
from .views import (
    FeeStructureListCreateView,
    FeeStructureRetrieveUpdateDestroyAPIView,
    PaymentRecordListCreateView,
    PaymentRecordRetrieveUpdateDestroyAPIView,
    StudentFeeView,
)

urlpatterns = [
    path('structure/', FeeStructureListCreateView.as_view(), name='fee-structure-list-create'),
    path('structure/<int:pk>/', FeeStructureRetrieveUpdateDestroyAPIView.as_view(), name='fee-structure-retrieve-update-destroy'),
    path('payment/', PaymentRecordListCreateView.as_view(), name='payment-record-list-create'),
    path('payment/<int:pk>/', PaymentRecordRetrieveUpdateDestroyAPIView.as_view(), name='payment-record-retrieve-update-destroy'),
    path('student/<int:student_id>/', StudentFeeView.as_view(), name='student-fee'),
]
