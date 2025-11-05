from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Classroom, TimeSlot, Timetable
from .serializers import ClassroomSerializer, TimeSlotSerializer, TimetableSerializer
from .permissions import IsAdminOrReadOnly

class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classrooms to be viewed or edited.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class TimeSlotViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows time slots to be viewed or edited.
    """
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class TimetableViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows timetables to be viewed or edited.
    """
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Timetable.objects.all()
        elif user.role == 'Faculty':
            return Timetable.objects.filter(department=user.faculty.department)
        elif user.role == 'Student':
            return Timetable.objects.filter(department=user.student.department, semester=user.student.semester)
        return Timetable.objects.none()
