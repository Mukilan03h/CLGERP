from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Hostel, Room, Allocation
from .serializers import HostelSerializer, RoomSerializer, AllocationSerializer
from .permissions import IsAdminUser, IsStudentOwner

class HostelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows hostels to be viewed or edited.
    """
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class AllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows allocations to be viewed or edited.
    """
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsStudentOwner]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            return Allocation.objects.filter(student__user=user)
        return Allocation.objects.all()
