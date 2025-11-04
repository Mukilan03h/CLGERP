from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vehicle, Route, TransportAllocation
from students.models import Student, Department
from auth_app.models import User

class TransportModelTest(APITestCase):
    def setUp(self):
        self.vehicle = Vehicle.objects.create(vehicle_no='XYZ-123', vehicle_type='Bus', capacity=50)
        self.route = Route.objects.create(name='Route 1', stops='Stop 1, Stop 2')
        department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(name='John Doe', roll_no='123', department=department, semester=1)

    def test_transport_allocation_creation(self):
        allocation = TransportAllocation.objects.create(student=self.student, route=self.route, vehicle=self.vehicle)
        self.assertEqual(TransportAllocation.objects.count(), 1)
        self.assertEqual(allocation.student.name, 'John Doe')

class TransportAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.student_user = User.objects.create_user(username='student', password='password', role='Student')
        department = Department.objects.create(name='Computer Science', code='CS')
        self.student = Student.objects.create(user=self.student_user, name='John Doe', roll_no='123', department=department, semester=1)
        self.vehicle = Vehicle.objects.create(vehicle_no='XYZ-123', vehicle_type='Bus', capacity=50)
        self.route = Route.objects.create(name='Route 1', stops='Stop 1, Stop 2')
        self.allocation = TransportAllocation.objects.create(student=self.student, route=self.route, vehicle=self.vehicle)

    def test_admin_can_create_vehicle(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('vehicle-list')
        data = {'vehicle_no': 'ABC-456', 'vehicle_type': 'Van', 'capacity': 20}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_student_cannot_create_vehicle(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('vehicle-list')
        data = {'vehicle_no': 'ABC-456', 'vehicle_type': 'Van', 'capacity': 20}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_student_can_view_own_allocation(self):
        self.client.force_authenticate(user=self.student_user)
        url = reverse('transportallocation-detail', kwargs={'pk': self.allocation.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_view_other_allocation(self):
        other_student_user = User.objects.create_user(username='other_student', password='password', role='Student')
        department = Department.objects.create(name='Mechanical', code='ME')
        other_student = Student.objects.create(user=other_student_user, name='Jane Doe', roll_no='456', department=department, semester=1)
        other_allocation = TransportAllocation.objects.create(student=other_student, route=self.route, vehicle=self.vehicle)
        self.client.force_authenticate(user=self.student_user)
        url = reverse('transportallocation-detail', kwargs={'pk': other_allocation.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
