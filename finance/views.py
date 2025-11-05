from rest_framework import viewsets
from .models import FeeStructure, FeePayment, Expense
from .serializers import FeeStructureSerializer, FeePaymentSerializer, ExpenseSerializer
from .permissions import IsAdminOrReadOnly, IsStudentOwner
from rest_framework.permissions import IsAuthenticated

class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.all()
    serializer_class = FeeStructureSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class FeePaymentViewSet(viewsets.ModelViewSet):
    queryset = FeePayment.objects.all()
    serializer_class = FeePaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return FeePayment.objects.all()
        elif user.role == 'Student':
            return FeePayment.objects.filter(student__user=user)
        return FeePayment.objects.none()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsStudentOwner]
        return super().get_permissions()

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
