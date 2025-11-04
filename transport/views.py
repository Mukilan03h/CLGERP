from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Vehicle, Route, TransportAllocation
from .serializers import VehicleSerializer, RouteSerializer, TransportAllocationSerializer
from .permissions import IsAdminUser, IsStudentOwner

class VehicleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vehicles to be viewed or edited.
    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows routes to be viewed or edited.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class TransportAllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows transport allocations to be viewed or edited.
    """
    queryset = TransportAllocation.objects.all()
    serializer_class = TransportAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            return TransportAllocation.objects.filter(student__user=user)
        return TransportAllocation.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAdminUser | IsStudentOwner]
        return super().get_permissions()
