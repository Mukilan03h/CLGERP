from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Faculty, LeaveRequest
from students.models import Department
from auth_app.models import User
import datetime

class FacultyPermissionsTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.other_faculty_user = User.objects.create_user(username='other_faculty', password='password', role='Faculty')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.other_department = Department.objects.create(name='Electrical Engineering', code='EE')

        self.faculty = Faculty.objects.create(user=self.faculty_user, name='Test Faculty', department=self.department, designation='Professor')
        self.other_faculty = Faculty.objects.create(user=self.other_faculty_user, name='Other Faculty', department=self.other_department, designation='Assistant Professor')

        self.leave_request = LeaveRequest.objects.create(faculty=self.faculty, start_date=datetime.date.today(), end_date=datetime.date.today(), reason='Sick')

    def test_admin_can_list_all_faculty(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('faculty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_faculty_can_list_faculty_in_their_department(self):
        self.client.force_authenticate(user=self.faculty_user)
        response = self.client.get(reverse('faculty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Faculty')

    def test_student_can_list_faculty_in_their_department(self):
        from students.models import Student
        Student.objects.create(user=self.student_user, name='Test Student', roll_no='123', department=self.department, semester=1, guardian_info='Test Guardian')
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(reverse('faculty-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Faculty')

    def test_admin_can_create_faculty(self):
        self.client.force_authenticate(user=self.admin_user)
        new_user = User.objects.create_user(username='new_faculty', password='password', role='Faculty')
        data = {'user': new_user.id, 'name': 'New Faculty', 'department': self.department.id, 'designation': 'Lecturer'}
        response = self.client.post(reverse('faculty-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_faculty_cannot_create_faculty(self):
        self.client.force_authenticate(user=self.faculty_user)
        new_user = User.objects.create_user(username='new_faculty_2', password='password', role='Faculty')
        data = {'user': new_user.id, 'name': 'New Faculty', 'department': self.department.id, 'designation': 'Lecturer'}
        response = self.client.post(reverse('faculty-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_faculty_can_view_own_leave_requests(self):
        self.client.force_authenticate(user=self.faculty_user)
        response = self.client.get(reverse('leaverequest-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_faculty_cannot_view_other_faculty_leave_requests(self):
        self.client.force_authenticate(user=self.other_faculty_user)
        response = self.client.get(reverse('leaverequest-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_faculty_cannot_update_other_faculty_profile(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'name': 'Updated Name'}
        response = self.client.patch(reverse('faculty-detail', kwargs={'pk': self.other_faculty.pk}), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_faculty_cannot_delete_other_faculty_profile(self):
        self.client.force_authenticate(user=self.faculty_user)
        response = self.client.delete(reverse('faculty-detail', kwargs={'pk': self.other_faculty.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
