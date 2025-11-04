from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Exam, Marks, Result
from .serializers import ExamSerializer, MarksSerializer, ResultSerializer

class ExamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows exams to be viewed or edited.
    """
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class MarksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows marks to be viewed or edited.
    """
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer

class ResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows results to be viewed or edited.
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

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
