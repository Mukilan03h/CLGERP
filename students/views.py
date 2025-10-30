from rest_framework import generics
from .models import Student
from .serializers import StudentSerializer
from auth_app.middleware import StandardizedResponseMiddleware

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class StudentByRollNoView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'roll_no'
    renderer_classes = [StandardizedResponseMiddleware]
