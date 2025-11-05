from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Hostel, Room, Allocation
from .serializers import HostelSerializer, RoomSerializer, AllocationSerializer
from .permissions import IsAdminOrReadOnly, IsStudentOwner

class HostelViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows hostels to be viewed or edited.
    """
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class AllocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows allocations to be viewed or edited.
    """
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Allocation.objects.all()
        elif user.role == 'Student':
            return Allocation.objects.filter(student__user=user)
        return Allocation.objects.none()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsAdminOrReadOnly | IsStudentOwner]
        return super().get_permissions()
