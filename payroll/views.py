from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Salary, Payslip, PayslipEntry
from .serializers import SalarySerializer, PayslipSerializer, PayslipEntrySerializer
from .permissions import IsAdminUser, IsOwnerOrAdmin

class SalaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows salaries to be viewed or edited.
    - Admins can perform any action.
    - Faculty can view their own salary.
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Salary.objects.all()
        elif hasattr(user, 'faculty'):
            return Salary.objects.filter(faculty=user.faculty)
        return Salary.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()

class PayslipViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows payslips to be viewed or edited.
    - Admins can perform any action.
    - Faculty can view their own payslips.
    """
    queryset = Payslip.objects.all()
    serializer_class = PayslipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Payslip.objects.all()
        elif hasattr(user, 'faculty'):
            return Payslip.objects.filter(faculty=user.faculty)
        return Payslip.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()

class PayslipEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows payslip entries to be viewed or edited.
    - Admins can perform any action.
    - Faculty can view entries related to their own payslips.
    """
    queryset = PayslipEntry.objects.all()
    serializer_class = PayslipEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return PayslipEntry.objects.all()
        elif hasattr(user, 'faculty'):
            return PayslipEntry.objects.filter(payslip__faculty=user.faculty)
        return PayslipEntry.objects.none()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()
