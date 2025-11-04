from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Classroom, TimeSlot, Timetable
from .serializers import ClassroomSerializer, TimeSlotSerializer, TimetableSerializer
from .permissions import IsAdminUser, IsFacultyUser, IsStudentUser, IsFacultyOwner

class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classrooms to be viewed or edited.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class TimeSlotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows time slots to be viewed or edited.
    """
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class TimetableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows timetables to be viewed or edited.
    """
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            return Timetable.objects.filter(department=user.student.department, semester=user.student.semester)
        elif user.role == 'Faculty':
            return Timetable.objects.filter(faculty__user=user)
        return Timetable.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser | (IsFacultyUser & IsFacultyOwner)]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
