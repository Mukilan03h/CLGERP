from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Route, TransportAllocation
from .serializers import VehicleSerializer, RouteSerializer, TransportAllocationSerializer
from .permissions import IsAdminOrReadOnly

class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vehicles to be viewed or edited.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows routes to be viewed or edited.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class TransportAllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transport allocations to be viewed or edited.
    """
    queryset = TransportAllocation.objects.all()
    serializer_class = TransportAllocationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return TransportAllocation.objects.all()
        elif user.role == 'Student':
            return TransportAllocation.objects.filter(student__user=user)
        return TransportAllocation.objects.none()
