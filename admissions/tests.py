from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Application, Admission
from students.models import Student, Department
from auth_app.models import User

class AdmissionsWorkflowTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.admissions_officer = User.objects.create_user(username='admissions', password='password', role='AdmissionOfficer')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        self.department = Department.objects.create(name='Computer Science', code='CS')
        self.application = Application.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            date_of_birth='2000-01-01',
            address='123 Test St',
            previous_education='Test School',
            department=self.department
        )

    def test_admissions_officer_can_approve_application(self):
        self.client.force_authenticate(user=self.admissions_officer)
        url = reverse('application-approve', kwargs={'pk': self.application.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'accepted')
        self.assertTrue(Student.objects.filter(roll_no=f'STU{self.application.id}').exists())
        self.assertTrue(Admission.objects.filter(application=self.application).exists())

    def test_admissions_officer_can_reject_application(self):
        self.client.force_authenticate(user=self.admissions_officer)
        url = reverse('application-reject', kwargs={'pk': self.application.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'rejected')

    def test_student_cannot_approve_application(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('application-approve', kwargs={'pk': self.application.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_cannot_reject_application(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('application-reject', kwargs={'pk': self.application.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
