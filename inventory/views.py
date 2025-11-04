from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import InventoryItem, Asset
from .serializers import InventoryItemSerializer, AssetSerializer
from .permissions import IsAdminUser

class InventoryItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows inventory items to be viewed or edited.
    """
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class AssetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows assets to be viewed or edited.
    """
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
