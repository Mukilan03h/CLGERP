from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Subject, Attendance
from students.models import Student, Department
from auth_app.models import User
import datetime

class AttendanceTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role='Admin'
        )
        self.client.force_authenticate(user=self.user)
        self.department = Department.objects.create(
            name='Computer Science',
            code='CS'
        )
        self.student = Student.objects.create(
            name='Test Student',
            roll_no='12345',
            department=self.department,
            semester=1
        )
        self.subject = Subject.objects.create(
            name='Data Structures',
            code='CS101',
            department=self.department,
            semester=1
        )
        self.attendance = Attendance.objects.create(
            student=self.student,
            subject=self.subject,
            date=datetime.date.today(),
            status='present'
        )

    def test_create_subject(self):
        url = reverse('subject-list')
        data = {
            'name': 'Algorithms',
            'code': 'CS102',
            'department': self.department.id,
            'semester': 1
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(), 2)

    def test_get_subjects(self):
        url = reverse('subject-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_attendance(self):
        url = reverse('attendance-list')
        data = {
            'student': self.student.id,
            'subject': self.subject.id,
            'date': datetime.date.today(),
            'status': 'absent'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 2)

    def test_get_attendance(self):
        url = reverse('attendance-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
