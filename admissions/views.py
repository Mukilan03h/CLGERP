from rest_framework import viewsets
from .models import Application, Admission
from .serializers import ApplicationSerializer, AdmissionSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
