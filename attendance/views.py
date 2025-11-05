from rest_framework import viewsets
from .models import Subject, Attendance
from .serializers import SubjectSerializer, AttendanceSerializer
from .permissions import IsAdminOrReadOnly, IsFacultyOrReadOnly, IsStudentOwner
from rest_framework.permissions import IsAuthenticated

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Subject.objects.all()
        elif user.role == 'Faculty':
            return Subject.objects.filter(department=user.faculty.department)
        elif user.role == 'Student':
            return Subject.objects.filter(department=user.student.department)
        return Subject.objects.none()

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsFacultyOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            return Attendance.objects.filter(student__user=user)
        elif user.role == 'Faculty':
            return Attendance.objects.filter(subject__in=user.faculty.subjects.all())
        return Attendance.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsFacultyOrReadOnly]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsStudentOwner]
        return super().get_permissions()
