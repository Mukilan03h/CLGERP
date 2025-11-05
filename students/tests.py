from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Student, Department
from auth_app.models import User

class StudentPermissionsTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        self.other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')

        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.other_department = Department.objects.create(name='Electrical Engineering', code='EE')

        self.student = Student.objects.create(user=self.student_user, name='Test Student', roll_no='123', department=self.department, semester=1, guardian_info='Test Guardian')
        self.other_student = Student.objects.create(user=self.other_student_user, name='Other Student', roll_no='456', department=self.other_department, semester=1, guardian_info='Other Guardian')

    def test_admin_can_list_all_students(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_faculty_can_list_students_in_their_department(self):
        from faculty.models import Faculty
        Faculty.objects.create(user=self.faculty_user, name='Test Faculty', department=self.department, designation='Professor')
        self.client.force_authenticate(user=self.faculty_user)
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Student')

    def test_student_can_only_see_their_own_profile(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Student')

    def test_student_cannot_see_other_student_profile(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('student-detail', kwargs={'pk': self.other_student.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_create_student(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New Student', 'roll_no': '789', 'department': self.department.id, 'semester': 1, 'guardian_info': 'New Guardian'}
        response = self.client.post(reverse('student-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_student(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'name': 'New Student', 'roll_no': '789', 'department': self.department.id, 'semester': 1, 'guardian_info': 'New Guardian'}
        response = self.client.post(reverse('student-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
