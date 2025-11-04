from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Exam, Marks, Result
from students.models import Student, Department
from attendance.models import Subject

class ExaminationModelTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(name='John Doe', roll_no='123', department=self.department, semester=1)
        self.subject = Subject.objects.create(name='Data Structures', code='CS101', semester=1)
        self.exam = Exam.objects.create(name='Mid Term', date='2024-01-01')
        self.exam.subjects.add(self.subject)

    def test_exam_creation(self):
        self.assertEqual(Exam.objects.count(), 1)
        self.assertEqual(self.exam.name, 'Mid Term')

    def test_marks_creation(self):
        marks = Marks.objects.create(exam=self.exam, student=self.student, subject=self.subject, marks=85)
        self.assertEqual(Marks.objects.count(), 1)
        self.assertEqual(marks.marks, 85)

    def test_result_creation(self):
        result = Result.objects.create(exam=self.exam, student=self.student, total_marks=85, percentage=85.0, grade='A')
        self.assertEqual(Result.objects.count(), 1)
        self.assertEqual(result.grade, 'A')

class ExaminationAPITest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(name='John Doe', roll_no='123', department=self.department, semester=1)
        self.subject1 = Subject.objects.create(name='Data Structures', code='CS101', semester=1)
        self.subject2 = Subject.objects.create(name='Algorithms', code='CS102', semester=1)
        self.exam = Exam.objects.create(name='Mid Term', date='2024-01-01')
        self.exam.subjects.add(self.subject1, self.subject2)

    def test_get_exams(self):
        url = reverse('exam-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_exam(self):
        url = reverse('exam-list')
        data = {'name': 'Final Term', 'date': '2024-05-01', 'subjects': [self.subject1.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_marks(self):
        url = reverse('marks-list')
        data = {'exam': self.exam.id, 'student': self.student.id, 'subject': self.subject1.id, 'marks': 85}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_result(self):
        Marks.objects.create(exam=self.exam, student=self.student, subject=self.subject1, marks=85)
        Marks.objects.create(exam=self.exam, student=self.student, subject=self.subject2, marks=95)
        url = reverse('result-list')
        data = {'exam': self.exam.id, 'student': self.student.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = Result.objects.get(exam=self.exam, student=self.student)
        self.assertEqual(result.total_marks, 180)
        self.assertEqual(result.percentage, 90.0)
        self.assertEqual(result.grade, 'A')
