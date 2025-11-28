"""
Tests complets pour l'API utilisateur et authentification
"""
import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


class UserAuthenticationTests(TestCase):
    """Tests pour l'authentification des utilisateurs"""

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'first_name': 'John',
            'last_name': 'Doe',
        }

    def test_user_signup_success(self):
        """Test l'inscription réussie d'un utilisateur"""
        response = self.client.post(
            '/api/users/signup/',
            self.user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_signup_invalid_email(self):
        """Test l'inscription avec un email invalide"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        
        response = self.client.post(
            '/api/users/signup/',
            invalid_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_weak_password(self):
        """Test l'inscription avec un mot de passe faible"""
        weak_data = self.user_data.copy()
        weak_data['password'] = '123'
        
        response = self.client.post(
            '/api/users/signup/',
            weak_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_duplicate_email(self):
        """Test l'inscription avec un email existant"""
        # Créer le premier utilisateur
        User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='Existing',
            last_name='User'
        )
        
        response = self.client.post(
            '/api/users/signup/',
            self.user_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        """Test la connexion réussie"""
        # Créer un utilisateur
        User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!'
        )
        
        response = self.client.post(
            '/api/users/login/',
            {
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """Test la connexion avec des identifiants invalides"""
        User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!'
        )
        
        response = self.client.post(
            '/api/users/login/',
            {
                'email': 'test@example.com',
                'password': 'WrongPassword'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        """Test le rafraîchissement du token"""
        # Créer un utilisateur et obtenir les tokens
        User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!'
        )
        
        login_response = self.client.post(
            '/api/users/login/',
            {
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            },
            format='json'
        )
        
        refresh_token = login_response.data['refresh']
        
        # Rafraîchir le token
        response = self.client.post(
            '/api/users/token/refresh/',
            {'refresh': refresh_token},
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class UserProfileTests(TestCase):
    """Tests pour les profils utilisateur"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!',
            first_name='John',
            last_name='Doe'
        )

    def test_get_profile_authenticated(self):
        """Test la récupération du profil utilisateur authentifié"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/users/profile/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'John')

    def test_get_profile_unauthenticated(self):
        """Test l'accès au profil sans authentification"""
        response = self.client.get('/api/users/profile/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_profile(self):
        """Test la mise à jour du profil"""
        self.client.force_authenticate(user=self.user)
        
        response = self.client.patch(
            '/api/users/profile/',
            {
                'first_name': 'Jane',
                'learning_style': 'visual'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Jane')
        self.assertEqual(response.data['learning_style'], 'visual')

    def test_user_activity_logging(self):
        """Test l'enregistrement des activités utilisateur"""
        self.client.force_authenticate(user=self.user)
        
        # Faire une requête
        self.client.get('/api/users/profile/')
        
        # Vérifier que l'activité est enregistrée
        from apps.users.models import UserActivityLog
        activity = UserActivityLog.objects.filter(user=self.user).last()
        
        self.assertIsNotNone(activity)
        self.assertEqual(activity.action, 'GET')


class UserSettingsTests(TestCase):
    """Tests pour les paramètres utilisateur"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!'
        )
        self.client.force_authenticate(user=self.user)

    def test_get_settings(self):
        """Test la récupération des paramètres"""
        response = self.client.get('/api/users/settings/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_notification_preferences(self):
        """Test la mise à jour des préférences de notification"""
        response = self.client.patch(
            '/api/users/settings/',
            {
                'email_notifications': False,
                'push_notifications': True
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class TestPasswordManagement:
    """Tests pour la gestion des mots de passe"""

    def test_password_reset_request(self, client):
        """Test la demande de réinitialisation de mot de passe"""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPassword123!'
        )
        
        response = client.post(
            '/api/users/password-reset/',
            {'email': 'test@example.com'},
            format='json'
        )
        
        assert response.status_code == status.HTTP_200_OK

    def test_password_reset_nonexistent_user(self, client):
        """Test la réinitialisation pour un utilisateur inexistant"""
        response = client.post(
            '/api/users/password-reset/',
            {'email': 'nonexistent@example.com'},
            format='json'
        )
        
        # Devrait retourner 200 OK pour des raisons de sécurité
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestUserQueryOptimization:
    """Tests pour les optimisations de requêtes"""

    def test_profile_list_query_count(self, client, django_assert_num_queries):
        """Test que la liste des profils est optimisée"""
        # Créer 10 utilisateurs
        for i in range(10):
            User.objects.create_user(
                email=f'user{i}@example.com',
                password='password123'
            )
        
        user = User.objects.first()
        client.force_authenticate(user=user)
        
        # Devrait faire un nombre limité de requêtes
        with django_assert_num_queries(3):
            response = client.get('/api/users/profiles/')
            assert response.status_code == status.HTTP_200_OK
