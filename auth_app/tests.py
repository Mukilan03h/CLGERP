import pytest
from django.urls import reverse
from rest_framework import status
from auth_app.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_registration(client):
    url = reverse('register')
    data = {
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'Student'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_user_login(client):
    User.objects.create_user(username='testuser', password='testpassword')
    url = reverse('login')
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
