import pytest
from django.urls import reverse
from rest_framework import status
from students.models import Department, Student
from auth_app.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user():
    return User.objects.create_user(username='admin', password='password', role='Admin')

@pytest.mark.django_db
def test_create_student(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    department = Department.objects.create(name='Computer Science', code='CS')
    url = reverse('student-list')
    data = {
        'name': 'John Doe',
        'roll_no': 'CS101',
        'department': department.id,
        'semester': 1,
        'guardian_info': 'Jane Doe'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.filter(roll_no='CS101').exists()

@pytest.mark.django_db
def test_get_student(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    department = Department.objects.create(name='Computer Science', code='CS')
    student = Student.objects.create(
        name='John Doe',
        roll_no='CS101',
        department=department,
        semester=1,
        guardian_info='Jane Doe'
    )
    url = reverse('student-detail', kwargs={'pk': student.id})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'John Doe'
