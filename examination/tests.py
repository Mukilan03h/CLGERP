from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Exam, Marks, Result
from students.models import Student, Department
from attendance.models import Subject
from auth_app.models import User
from faculty.models import Faculty

class ExaminationPermissionsTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        self.other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')

        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.other_department = Department.objects.create(name='Electrical Engineering', code='EE')

        self.student = Student.objects.create(user=self.student_user, name='Test Student', roll_no='123', department=self.department, semester=1, guardian_info='Test Guardian')
        self.other_student = Student.objects.create(user=self.other_student_user, name='Other Student', roll_no='456', department=self.other_department, semester=1, guardian_info='Other Guardian')

        self.faculty = Faculty.objects.create(user=self.faculty_user, name='Test Faculty', department=self.department, designation='Professor')

        self.subject1 = Subject.objects.create(name='Data Structures', code='CS101', department=self.department, semester=1)
        self.subject2 = Subject.objects.create(name='Algorithms', code='CS102', department=self.department, semester=1)
        self.faculty.subjects.add(self.subject1)

        self.exam = Exam.objects.create(name='Mid Term', date='2024-01-01')
        self.exam.subjects.add(self.subject1, self.subject2)

        self.marks = Marks.objects.create(exam=self.exam, student=self.student, subject=self.subject1, marks=85)
        self.result = Result.objects.create(exam=self.exam, student=self.student, total_marks=85, percentage=85.0, grade='A')

    def test_admin_can_list_all_exams(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('exam-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_list_exams_in_their_department(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('exam-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_can_view_own_marks(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('marks-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_view_other_marks(self):
        self.client.force_authenticate(user=self.other_student_user)
        response = self.client.get(reverse('marks-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_faculty_can_create_marks_for_own_subject(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'exam': self.exam.id, 'student': self.student.id, 'subject': self.subject1.id, 'marks': 85}
        response = self.client.post(reverse('marks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_marks_for_other_subject(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'exam': self.exam.id, 'student': self.student.id, 'subject': self.subject2.id, 'marks': 85}
        response = self.client.post(reverse('marks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_result(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('result-detail', kwargs={'pk': self.result.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_view_other_result(self):
        self.client.force_authenticate(user=self.other_student_user)
        response = self.client.get(reverse('result-detail', kwargs={'pk': self.result.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_create_exam(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'Final Exam', 'date': '2024-05-01', 'subjects': [self.subject1.id]}
        response = self.client.post(reverse('exam-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_exam(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'name': 'Final Exam', 'date': '2024-05-01', 'subjects': [self.subject1.id]}
        response = self.client.post(reverse('exam-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_marks_with_invalid_marks(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'exam': self.exam.id, 'student': self.student.id, 'subject': self.subject1.id, 'marks': 101}
        response = self.client.post(reverse('marks-list'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_student_cannot_update_marks(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'marks': 90}
        response = self.client.patch(reverse('marks-detail', kwargs={'pk': self.marks.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
