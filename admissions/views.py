from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Application, Admission
from .serializers import ApplicationSerializer, AdmissionSerializer
from .permissions import IsAdmissionsStaff
from rest_framework.permissions import IsAuthenticated
from auth_app.models import User
from students.models import Student
from django.utils.crypto import get_random_string

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['approve', 'reject']:
            self.permission_classes = [IsAuthenticated, IsAdmissionsStaff]
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        application = self.get_object()
        if application.status != 'pending':
            return Response({'status': 'application already reviewed'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = User.objects.create_user(
            username=application.email,
            password=get_random_string(12),
            role='Student'
        )

        # Create student
        student = Student.objects.create(
            user=user,
            name=f'{application.first_name} {application.last_name}',
            roll_no=f'STU{application.id}',
            department=application.department,
            semester=1,
            guardian_info='N/A'
        )

        # Create admission
        Admission.objects.create(application=application, student=student)

        application.status = 'accepted'
        application.save()
        return Response({'status': 'application approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        application = self.get_object()
        if application.status != 'pending':
            return Response({'status': 'application already reviewed'}, status=status.HTTP_400_BAD_REQUEST)

        application.status = 'rejected'
        application.save()
        return Response({'status': 'application rejected'})

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsAuthenticated, IsAdmissionsStaff]
