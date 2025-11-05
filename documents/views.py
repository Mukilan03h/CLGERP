from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Document, Certificate
from .serializers import DocumentSerializer, CertificateSerializer
from .permissions import IsOwnerOrAdmin, IsAdminUser

class DocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user-uploaded documents.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Document.objects.all()
        return Document.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def verify(self, request, pk=None):
        document = self.get_object()
        document.status = 'Verified'
        document.save()
        return Response({'status': 'document verified'})

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        document = self.get_object()
        document.status = 'Rejected'
        document.save()
        return Response({'status': 'document rejected'})

class CertificateViewSet(viewsets.ModelViewSet):
    """
    API endpoint for college-generated certificates.
    """
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Certificate.objects.all()
        return Certificate.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['retrieve', 'list']:
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()
