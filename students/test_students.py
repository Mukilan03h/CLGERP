import pytest
from django.urls import reverse
from rest_framework import status
from students.models import Department, Student

@pytest.mark.django_db
def test_create_student(client):
    department = Department.objects.create(name='Computer Science', code='CS')
    url = reverse('student-list-create')
    data = {
        'name': 'John Doe',
        'roll_no': 'CS101',
        'department': department.id,
        'semester': 1,
        'guardian_info': 'Jane Doe'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Student.objects.filter(roll_no='CS101').exists()

@pytest.mark.django_db
def test_get_student(client):
    department = Department.objects.create(name='Computer Science', code='CS')
    student = Student.objects.create(
        name='John Doe',
        roll_no='CS101',
        department=department,
        semester=1,
        guardian_info='Jane Doe'
    )
    url = reverse('student-retrieve-update-destroy', kwargs={'pk': student.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'John Doe'
