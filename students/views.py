from rest_framework import viewsets
from .models import Student
from .serializers import StudentSerializer
from .permissions import IsAdminOrReadOnly, IsOwner
from rest_framework.permissions import IsAuthenticated

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Student.objects.all()
        elif user.role == 'Faculty':
            return Student.objects.filter(department=user.faculty.department)
        elif user.role == 'Student':
            return Student.objects.filter(user=user)
        return Student.objects.none()

    def get_permissions(self):
        if self.request.user.role == 'Admin':
            return [IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        return super().get_permissions()
