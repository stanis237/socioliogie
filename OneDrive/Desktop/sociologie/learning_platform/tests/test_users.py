"""
Tests pour les modèles et API des utilisateurs
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    
    def test_user_registration(self):
        """Test l'enregistrement d'un nouvel utilisateur"""
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!'
        }
        response = client.post('/api/users/signup/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='test@example.com').exists()
    
    def test_user_registration_password_mismatch(self):
        """Test l'enregistrement avec mots de passe non-concordants"""
        client = APIClient()
        data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123!',
            'password_confirm': 'DifferentPassword123!'
        }
        response = client.post('/api/users/signup/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserProfile:
    
    def setup_method(self):
        """Créer un utilisateur de test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_get_user_profile(self):
        """Test la récupération du profil utilisateur"""
        response = self.client.get('/api/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
    
    def test_update_user_profile(self):
        """Test la mise à jour du profil"""
        data = {
            'first_name': 'Updated',
            'learning_style': 'visual'
        }
        response = self.client.put('/api/users/update_me/', data)
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.first_name == 'Updated'


@pytest.mark.django_db
class TestUserSettings:
    
    def setup_method(self):
        """Créer un utilisateur de test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='TestPassword123!'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_get_user_settings(self):
        """Test la récupération des paramètres"""
        response = self.client.get('/api/users/settings/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_update_user_settings(self):
        """Test la mise à jour des paramètres"""
        data = {
            'theme': 'dark',
            'language': 'en'
        }
        response = self.client.put('/api/users/settings/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['theme'] == 'dark'
