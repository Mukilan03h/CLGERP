from rest_framework import viewsets, permissions
from .models import Company, Job, Application
from .serializers import CompanySerializer, JobSerializer, ApplicationSerializer
from .permissions import IsAdminOrReadOnly, IsStudentOwner

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for companies. Admins can edit, others can only read.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for jobs. Admins can edit, others can only read.
    """
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for job applications.
    - Students can create applications for themselves.
    - Students can view/edit/delete their own applications.
    - Admins can view/edit/delete any application.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Application.objects.all()
        elif user.role == 'Student' and hasattr(user, 'student'):
            return Application.objects.filter(student=user.student)
        return Application.objects.none()

    def perform_create(self, serializer):
        # Allow students to apply for jobs for themselves
        if self.request.user.role == 'Student' and hasattr(self.request.user, 'student'):
            serializer.save(student=self.request.user.student)
        else:
            # Admins must specify the student
            serializer.save()

    def get_permissions(self):
        if self.request.user.role == 'Admin':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [permissions.IsAuthenticated(), IsStudentOwner()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsAdminOrReadOnly()]
