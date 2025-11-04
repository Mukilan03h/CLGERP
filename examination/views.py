from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Exam, Marks, Result
from .serializers import ExamSerializer, MarksSerializer, ResultSerializer
from .permissions import IsAdminUser, IsFacultyUser, IsStudentUser, IsStudentOwner, IsFacultyForSubject

class ExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows exams to be viewed or edited.
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser | IsFacultyUser]
        return super().get_permissions()

class MarksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows marks to be viewed or edited.
    """
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            return Marks.objects.filter(student__user=user)
        elif user.role == 'Faculty':
            return Marks.objects.filter(subject__in=user.faculty.subjects.all())
        return Marks.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            self.permission_classes = [IsAdminUser | (IsFacultyUser & IsFacultyForSubject)]
        elif self.action == 'destroy':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows results to be viewed or edited.
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Student':
            return Result.objects.filter(student__user=user)
        return Result.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminUser | IsFacultyUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAdminUser | IsFacultyUser | IsStudentOwner]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        exam_id = request.data.get('exam')
        student_id = request.data.get('student')

        # Calculate total marks
        marks = Marks.objects.filter(exam_id=exam_id, student_id=student_id)
        total_marks = sum([mark.marks for mark in marks])

        # Calculate percentage
        exam = Exam.objects.get(id=exam_id)
        num_subjects = exam.subjects.count()
        percentage = (total_marks / (num_subjects * 100)) * 100

        # Determine grade
        if percentage >= 90:
            grade = 'A'
        elif percentage >= 80:
            grade = 'B'
        elif percentage >= 70:
            grade = 'C'
        elif percentage >= 60:
            grade = 'D'
        else:
            grade = 'F'

        # Create result
        result = Result.objects.create(
            exam_id=exam_id,
            student_id=student_id,
            total_marks=total_marks,
            percentage=percentage,
            grade=grade
        )
        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
