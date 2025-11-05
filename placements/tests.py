from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Company, Job, Application
from auth_app.models import User
from students.models import Student, Department
from django.core.files.uploadedfile import SimpleUploadedFile

class PlacementAPITest(APITestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        # Department and Student
        self.department = Department.objects.create(name='Computer Science')
        self.student = Student.objects.create(name='John Doe', department=self.department, user=self.student_user, semester=1, guardian_info='Test Guardian')

        # Company, Job, and Application
        self.company = Company.objects.create(name='Tech Solutions')
        self.job = Job.objects.create(
            company=self.company,
            title='Junior Developer',
            description='An exciting opportunity.',
            application_deadline='2025-12-31'
        )
        self.application = Application.objects.create(job=self.job, student=self.student)

    def test_admin_can_create_company(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('company-list')
        data = {'name': 'New Company'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_company(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('company-list')
        data = {'name': 'Student Company'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_apply_for_job(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('application-list')
        new_job = Job.objects.create(
            company=self.company,
            title='Data Analyst',
            description='Another great job.',
            application_deadline='2025-12-31'
        )
        resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        data = {'job': new_job.pk, 'resume': resume}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_can_view_own_application(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('application-detail', kwargs={'pk': self.application.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_any_application(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('application-detail', kwargs={'pk': self.application.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
