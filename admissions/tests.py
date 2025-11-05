from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Application, Admission
from students.models import Student, Department
from auth_app.models import User

class AdmissionsTests(APITestCase):

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
        self.application = Application.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            date_of_birth='2000-01-01',
            address='123 Test St',
            previous_education='Test School'
        )
        self.admission = Admission.objects.create(
            application=self.application,
            student=self.student
        )

    def test_create_application(self):
        url = reverse('admission-application-list')
        data = {
            'first_name': 'New',
            'last_name': 'Applicant',
            'email': 'new@example.com',
            'phone_number': '0987654321',
            'date_of_birth': '2001-01-01',
            'address': '456 New Ave',
            'previous_education': 'New School'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 2)

    def test_get_applications(self):
        url = reverse('admission-application-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_admission(self):
        url = reverse('admission-list')
        new_application = Application.objects.create(
            first_name='Another',
            last_name='Applicant',
            email='another@example.com',
            phone_number='111222333',
            date_of_birth='2002-01-01',
            address='789 Another St',
            previous_education='Another School'
        )
        new_student = Student.objects.create(
            name='Another Student',
            roll_no='67890',
            department=self.department,
            semester=1
        )
        data = {
            'application': new_application.id,
            'student': new_student.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Admission.objects.count(), 2)

    def test_get_admissions(self):
        url = reverse('admission-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
