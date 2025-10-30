import pytest
from django.urls import reverse
from rest_framework import status
from .models import Program, Course, Syllabus

@pytest.mark.django_db
def test_create_program(client):
    url = reverse('program-list-create')
    data = {
        'name': 'Bachelor of Science',
        'code': 'BS',
        'duration': 4
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Program.objects.filter(code='BS').exists()

@pytest.mark.django_db
def test_get_program(client):
    program = Program.objects.create(
        name='Bachelor of Science',
        code='BS',
        duration=4
    )
    url = reverse('program-retrieve-update-destroy', kwargs={'pk': program.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Bachelor of Science'

@pytest.mark.django_db
def test_create_course(client):
    program = Program.objects.create(
        name='Bachelor of Science',
        code='BS',
        duration=4
    )
    url = reverse('course-list-create')
    data = {
        'name': 'Introduction to Computer Science',
        'code': 'CS101',
        'program': program.id,
        'credits': 3,
        'semester': 1
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.filter(code='CS101').exists()

@pytest.mark.django_db
def test_get_course(client):
    program = Program.objects.create(
        name='Bachelor of Science',
        code='BS',
        duration=4
    )
    course = Course.objects.create(
        name='Introduction to Computer Science',
        code='CS101',
        program=program,
        credits=3,
        semester=1
    )
    url = reverse('course-retrieve-update-destroy', kwargs={'pk': course.id})
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == 'Introduction to Computer Science'
