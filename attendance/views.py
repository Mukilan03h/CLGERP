from rest_framework import generics
from .models import Attendance, Subject
from .serializers import AttendanceSerializer, SubjectSerializer
from auth_app.middleware import StandardizedResponseMiddleware

class SubjectListCreateView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class SubjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class AttendanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    renderer_classes = [StandardizedResponseMiddleware]

    def get_queryset(self):
        return Attendance.objects.filter(student_id=self.kwargs['student_id'])

class AttendanceReportView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    renderer_classes = [StandardizedResponseMiddleware]

    def get_queryset(self):
        return Attendance.objects.filter(subject__semester=self.kwargs['semester'])
