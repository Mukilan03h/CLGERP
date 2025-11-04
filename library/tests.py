from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, BookIssue, Fine
from students.models import Student, Department
from auth_app.models import User
import datetime

class LibraryModelTest(APITestCase):
    def setUp(self):
        self.book = Book.objects.create(title='Test Book', author='Test Author', isbn='1234567890123')
        department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(name='John Doe', roll_no='123', department=department, semester=1)

    def test_book_issue_creation(self):
        due_date = datetime.date.today() + datetime.timedelta(days=14)
        book_issue = BookIssue.objects.create(book=self.book, student=self.student, due_date=due_date)
        self.assertEqual(BookIssue.objects.count(), 1)
        self.assertEqual(book_issue.book.title, 'Test Book')

class LibraryAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(user=self.student_user, name='John Doe', roll_no='123', department=department, semester=1)
        self.book = Book.objects.create(title='Test Book', author='Test Author', isbn='1234567890123')
        due_date = datetime.date.today() + datetime.timedelta(days=14)
        self.book_issue = BookIssue.objects.create(book=self.book, student=self.student, due_date=due_date)

    def test_admin_can_create_book(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('book-list')
        data = {'title': 'New Book', 'author': 'New Author', 'isbn': '9876543210987'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_book(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('book-list')
        data = {'title': 'New Book', 'author': 'New Author', 'isbn': '9876543210987'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_book_issue(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('bookissue-detail', kwargs={'pk': self.book_issue.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_view_other_book_issue(self):
        other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')
        department = Department.objects.create(name='Mechanical', code='ME')
        other_student = Student.objects.create(user=other_student_user, name='Jane Doe', roll_no='456', department=department, semester=1)
        due_date = datetime.date.today() + datetime.timedelta(days=14)
        other_book_issue = BookIssue.objects.create(book=self.book, student=other_student, due_date=due_date)
        self.client.force_authenticate(user=self.student_user)
        url = reverse('bookissue-detail', kwargs={'pk': other_book_issue.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
