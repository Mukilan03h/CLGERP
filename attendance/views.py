from rest_framework import viewsets
from .models import Subject, Attendance
from .serializers import SubjectSerializer, AttendanceSerializer
from rest_framework.permissions import IsAuthenticated

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
