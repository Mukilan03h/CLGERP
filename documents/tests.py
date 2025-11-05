from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Document, Certificate
from auth_app.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class DocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.document = Document.objects.create(user=self.user, document_type='ID Card', file='path/to/file.pdf')

    def test_document_creation(self):
        self.assertEqual(self.document.user, self.user)
        self.assertEqual(self.document.document_type, 'ID Card')
        self.assertEqual(self.document.status, 'Pending')

class DocumentAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')

        # A simple fake file
        self.fake_file = SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf")

        # Don't create the document here, it will be created in the test
        # self.document = Document.objects.create(user=self.student_user, document_type='Transcript', file=self.fake_file)

        self.list_create_url = reverse('document-list')

    def test_student_can_upload_document(self):
        self.client.force_authenticate(user=self.student_user)
        data = {'document_type': 'New ID', 'file': self.fake_file}
        response = self.client.post(self.list_create_url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_student_can_view_own_document(self):
        document = Document.objects.create(user=self.student_user, document_type='Transcript', file=self.fake_file)
        detail_url = reverse('document-detail', kwargs={'pk': document.pk})
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_verify_document(self):
        document = Document.objects.create(user=self.student_user, document_type='Transcript', file=self.fake_file)
        verify_url = reverse('document-verify', kwargs={'pk': document.pk})
        self.client.force_authenticate(user=self.student_user)
        response = self.client.post(verify_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_verify_document(self):
        document = Document.objects.create(user=self.student_user, document_type='Transcript', file=self.fake_file)
        verify_url = reverse('document-verify', kwargs={'pk': document.pk})
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(verify_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        document.refresh_from_db()
        self.assertEqual(document.status, 'Verified')

    def test_admin_can_list_all_documents(self):
        Document.objects.create(user=self.student_user, document_type='Transcript', file=self.fake_file)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
