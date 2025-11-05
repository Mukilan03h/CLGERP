from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ActivityLog
from auth_app.models import User
from .middleware import AuditTrailMiddleware
from django.contrib.auth.signals import user_logged_in

class AuditModelTest(TestCase):
    def test_log_creation(self):
        user = User.objects.create_user(username='testuser', password='password')
        log = ActivityLog.objects.create(user=user, action_type='Test', description='This is a test.')
        self.assertEqual(ActivityLog.objects.count(), 1)
        self.assertEqual(log.user, user)

class AuditAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        ActivityLog.objects.create(user=self.admin_user, action_type='Test', description='Admin test log.')

        self.logs_url = reverse('activitylog-list')

    def test_admin_can_view_logs(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.logs_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_student_cannot_view_logs(self):
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.logs_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class AuditIntegrationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='logger', password='password')

    def test_login_signal_creates_log(self):
        request = self.factory.get('/fake-login')
        request.user = self.user
        user_logged_in.send(sender=self.user.__class__, request=request, user=self.user)
        self.assertEqual(ActivityLog.objects.count(), 1)
        log = ActivityLog.objects.first()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action_type, 'Login')

    def test_middleware_creates_log_on_post(self):
        def get_response(request):
            return None # Dummy response function

        middleware = AuditTrailMiddleware(get_response)
        request = self.factory.post('/fake-path')
        request.user = self.user
        middleware(request)

        self.assertEqual(ActivityLog.objects.count(), 1)
        log = ActivityLog.objects.first()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action_type, 'Create')
