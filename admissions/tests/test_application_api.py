import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from auth_app.models import User
from admissions.models import Application
from workflow.models import Workflow, Stage, Transition

@pytest.mark.django_db
class TestApplicationTransitionAPI:
    def setup_method(self):
        self.client = APIClient()

        # Users
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.officer_user = User.objects.create_user(username='officer', password='password', role='AdmissionOfficer')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')

        # Workflow setup
        self.workflow = Workflow.objects.create(name='Admission Workflow')
        self.stage1 = Stage.objects.create(workflow=self.workflow, name='Pending', order=1)
        self.stage2 = Stage.objects.create(workflow=self.workflow, name='Reviewed', order=2)
        self.stage3 = Stage.objects.create(workflow=self.workflow, name='Approved', order=3)

        # Transitions
        self.transition1 = Transition.objects.create(workflow=self.workflow, from_stage=self.stage1, to_stage=self.stage2, role='AdmissionOfficer')
        self.transition2 = Transition.objects.create(workflow=self.workflow, from_stage=self.stage2, to_stage=self.stage3, role='Admin')

        # Application
        self.application = Application.objects.create(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            date_of_birth='2000-01-01',
            address='123 Test St',
            previous_education='Test School',
            workflow=self.workflow,
            current_stage=self.stage1
        )

        self.transition_url = reverse('admission-application-transition', kwargs={'pk': self.application.pk})

    def test_authorized_user_can_transition_application(self):
        self.client.force_authenticate(user=self.officer_user)
        data = {'to_stage': self.stage2.pk}
        response = self.client.post(self.transition_url, data)

        assert response.status_code == status.HTTP_200_OK
        self.application.refresh_from_db()
        assert self.application.current_stage == self.stage2

    def test_unauthorized_user_cannot_transition_application(self):
        self.client.force_authenticate(user=self.faculty_user) # Faculty role is not in the transition
        data = {'to_stage': self.stage2.pk}
        response = self.client.post(self.transition_url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        self.application.refresh_from_db()
        assert self.application.current_stage == self.stage1 # Stage should not change

    def test_invalid_transition_is_rejected(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'to_stage': self.stage3.pk} # Admin can't move from stage1 to stage3 directly
        response = self.client.post(self.transition_url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        self.application.refresh_from_db()
        assert self.application.current_stage == self.stage1

    def test_transition_without_workflow_fails(self):
        app_no_workflow = Application.objects.create(
            first_name='No',
            last_name='Workflow',
            email='nowf@test.com',
            phone_number='1234567890',
            date_of_birth='2000-01-01',
            address='123 Test St',
            previous_education='Test School'
        )
        url = reverse('admission-application-transition', kwargs={'pk': app_no_workflow.pk})
        self.client.force_authenticate(user=self.admin_user)
        data = {'to_stage': self.stage1.pk}

        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unauthenticated_user_cannot_transition(self):
        data = {'to_stage': self.stage2.pk}
        response = self.client.post(self.transition_url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
