from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Exam, Marks, Result
from students.models import Student, Department
from attendance.models import Subject
from auth_app.models import User
from faculty.models import Faculty

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
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        self.student = Student.objects.create(user=self.student_user, name='John Doe', roll_no='123', department=self.department, semester=1)
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.faculty = Faculty.objects.create(user=self.faculty_user, name='Dr. Smith', department=self.department, designation='Professor')
        self.subject1 = Subject.objects.create(name='Data Structures', code='CS101', semester=1)
        self.subject2 = Subject.objects.create(name='Algorithms', code='CS102', semester=1)
        self.faculty.subjects.add(self.subject1)
        self.exam = Exam.objects.create(name='Mid Term', date='2024-01-01')
        self.exam.subjects.add(self.subject1, self.subject2)

    def test_student_can_view_own_marks(self):
        Marks.objects.create(exam=self.exam, student=self.student, subject=self.subject1, marks=85)
        self.client.force_authenticate(user=self.student_user)
        url = reverse('marks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_view_other_marks(self):
        other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')
        other_student = Student.objects.create(user=other_student_user, name='Jane Doe', roll_no='456', department=self.department, semester=1)
        Marks.objects.create(exam=self.exam, student=other_student, subject=self.subject1, marks=90)
        self.client.force_authenticate(user=self.student_user)
        url = reverse('marks-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_faculty_can_create_marks_for_own_subject(self):
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('marks-list')
        data = {'exam': self.exam.id, 'student': self.student.id, 'subject': self.subject1.id, 'marks': 85}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_marks_for_other_subject(self):
        self.client.force_authenticate(user=self.faculty_user)
        url = reverse('marks-list')
        data = {'exam': self.exam.id, 'student': self.student.id, 'subject': self.subject2.id, 'marks': 85}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
