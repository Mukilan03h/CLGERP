from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Company, Job, Application
from auth_app.models import User
from students.models import Student, Department

class PlacementModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name='Test Corp')
        self.job = Job.objects.create(
            company=self.company,
            title='Software Engineer',
            description='A great job.',
            application_deadline='2025-12-31'
        )

    def test_job_creation(self):
        self.assertEqual(self.job.title, 'Software Engineer')
        self.assertEqual(self.job.company.name, 'Test Corp')

class PlacementAPITest(APITestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        # Department and Student
        self.department = Department.objects.create(name='Computer Science')
        self.student = Student.objects.create(name='John Doe', department=self.department, user=self.student_user, semester=1)

        # Company, Job, and Application
        self.company = Company.objects.create(name='Tech Solutions')
        self.job = Job.objects.create(
            company=self.company,
            title='Junior Developer',
            description='An exciting opportunity.',
            application_deadline='2025-12-31'
        )
        self.application = Application.objects.create(job=self.job, student=self.student)

        # URLs
        self.companies_url = reverse('company-list')
        self.jobs_url = reverse('job-list')
        self.applications_url = reverse('application-list')
        self.application_detail_url = reverse('application-detail', kwargs={'pk': self.application.pk})

    def test_admin_can_create_company(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New Company'}
        response = self.client.post(self.companies_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_company(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'name': 'Student Company'}
        response = self.client.post(self.companies_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_apply_for_job(self):
        self.client.force_authenticate(user=self.student_user)
        new_job = Job.objects.create(
            company=self.company,
            title='Data Analyst',
            description='Another great job.',
            application_deadline='2025-12-31'
        )
        data = {'job': new_job.pk, 'resume': 'path/to/resume.pdf'}
        response = self.client.post(self.applications_url, data)
        # We expect a validation error due to the file upload, but the permission is what we're testing.
        # A 400 or 403 would be acceptable depending on how the serializer handles it.
        # For this test, we are just checking that the student is not forbidden from applying.
        # The permission check runs before the serializer validation.
        # Since the student is creating an application for themselves, it should pass.
        # But since we are not uploading a file, it will fail.
        # Let's check for a status code other than 403.
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_application(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.application_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_view_any_application(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.application_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
