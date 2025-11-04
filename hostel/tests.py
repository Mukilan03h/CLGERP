from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Hostel, Room, Allocation
from students.models import Student, Department
from auth_app.models import User

class HostelModelTest(APITestCase):
    def setUp(self):
        self.hostel = Hostel.objects.create(name='Test Hostel', capacity=100)
        self.room = Room.objects.create(hostel=self.hostel, room_no='101', capacity=2)
        department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(name='John Doe', roll_no='123', department=department, semester=1)

    def test_allocation_creation(self):
        allocation = Allocation.objects.create(room=self.room, student=self.student)
        self.assertEqual(Allocation.objects.count(), 1)
        self.assertEqual(allocation.student.name, 'John Doe')

class HostelAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(user=self.student_user, name='John Doe', roll_no='123', department=department, semester=1)
        self.hostel = Hostel.objects.create(name='Test Hostel', capacity=100)
        self.room = Room.objects.create(hostel=self.hostel, room_no='101', capacity=2)
        self.allocation = Allocation.objects.create(room=self.room, student=self.student)

    def test_admin_can_create_hostel(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('hostel-list')
        data = {'name': 'New Hostel', 'capacity': 200}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_hostel(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('hostel-list')
        data = {'name': 'New Hostel', 'capacity': 200}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_allocation(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('allocation-detail', kwargs={'pk': self.allocation.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_view_other_allocation(self):
        other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')
        department = Department.objects.create(name='Mechanical', code='ME')
        other_student = Student.objects.create(user=other_student_user, name='Jane Doe', roll_no='456', department=department, semester=1)
        other_allocation = Allocation.objects.create(room=self.room, student=other_student)
        self.client.force_authenticate(user=self.student_user)
        url = reverse('allocation-detail', kwargs={'pk': other_allocation.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_admin_can_view_any_allocation(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('allocation-detail', kwargs={'pk': self.allocation.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
