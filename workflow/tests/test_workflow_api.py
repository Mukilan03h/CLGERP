import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from auth_app.models import User
from workflow.models import Workflow

@pytest.mark.django_db
class TestWorkflowAPI:
    def setup_method(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.faculty_user = User.objects.create_user(username='faculty', password='password', role='Faculty')
        self.workflow = Workflow.objects.create(name='Test Workflow', description='A test workflow')
        self.workflow_url = reverse('workflow-list') # Note: DRF router generates this name
        self.workflow_detail_url = reverse('workflow-detail', kwargs={'pk': self.workflow.pk})

    def test_admin_can_list_workflows(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.workflow_url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_non_admin_cannot_list_workflows(self):
        self.client.force_authenticate(user=self.faculty_user)
        response = self.client.get(self.workflow_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unauthenticated_user_cannot_list_workflows(self):
        response = self.client.get(self.workflow_url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_admin_can_create_workflow(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'name': 'New Workflow', 'description': 'A new test workflow'}
        response = self.client.post(self.workflow_url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Workflow.objects.count() == 2

    def test_non_admin_cannot_create_workflow(self):
        self.client.force_authenticate(user=self.faculty_user)
        data = {'name': 'New Workflow'}
        response = self.client.post(self.workflow_url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete_workflow(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.workflow_detail_url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Workflow.objects.count() == 0
