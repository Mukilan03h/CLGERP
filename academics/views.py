from rest_framework import generics
from .models import Program, Course, Syllabus
from .serializers import ProgramSerializer, CourseSerializer, SyllabusSerializer
from auth_app.middleware import StandardizedResponseMiddleware

class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class ProgramRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class SyllabusListCreateView(generics.ListCreateAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class SyllabusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    renderer_classes = [StandardizedResponseMiddleware]
