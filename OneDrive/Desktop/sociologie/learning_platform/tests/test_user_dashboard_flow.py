import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.users.models import CustomUser

@pytest.mark.django_db
def test_signup_login_dashboard_flow():
    client = APIClient()

    # Test signup
    signup_url = reverse('signup_view')
    signup_data = {
        "email": "testuser@example.com",
        "password": "StrongPassw0rd!",
        "password_confirm": "StrongPassw0rd!",
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post(signup_url, signup_data, format='json')
    assert response.status_code == 201
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert 'user' in response.data
    user_id = response.data['user']['id']

    # Test login with the same user
    login_url = reverse('login_view')
    login_data = {
        "email": "testuser@example.com",
        "password": "StrongPassw0rd!"
    }
    response = client.post(login_url, login_data, format='json')
    assert response.status_code == 200
    access_token = response.data['access']
    assert access_token is not None

    # Access dashboard/profile endpoint with token
    profile_url = reverse('profile_view')
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = client.get(profile_url)
    assert response.status_code == 200
    assert response.data['id'] == user_id
    assert response.data['email'] == "testuser@example.com"
    assert response.data['first_name'] == "Test"
    assert response.data['last_name'] == "User"
