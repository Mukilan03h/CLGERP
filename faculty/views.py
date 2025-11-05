from rest_framework import viewsets
from .models import Faculty, LeaveRequest
from .serializers import FacultySerializer, LeaveRequestSerializer
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated

class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Faculty.objects.all()
        elif user.role == 'Faculty':
            return Faculty.objects.filter(department=user.faculty.department)
        elif user.role == 'Student':
            return Faculty.objects.filter(department=user.student.department)
        return Faculty.objects.none()

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return LeaveRequest.objects.all()
        return LeaveRequest.objects.filter(faculty__user=user)
