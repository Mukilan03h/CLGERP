from rest_framework import viewsets
from .models import Item, Supplier
from .serializers import ItemSerializer, SupplierSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
