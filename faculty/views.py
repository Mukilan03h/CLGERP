from rest_framework import generics
from .models import Faculty, LeaveRequest
from .serializers import FacultySerializer, LeaveRequestSerializer
from auth_app.middleware import StandardizedResponseMiddleware

class FacultyListCreateView(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    renderer_classes = [StandardizedResponseMiddleware]

class FacultyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    renderer_classes = [StandardizedResponseMiddleware]

class LeaveRequestListCreateView(generics.ListCreateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    renderer_classes = [StandardizedResponseMiddleware]

class LeaveRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    renderer_classes = [StandardizedResponseMiddleware]
