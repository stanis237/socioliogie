from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, Historique

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = UserProfile.objects.get(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.level, 'beginner')
        self.assertEqual(self.profile.school_level, 'secondary')
        self.assertEqual(self.profile.points, 0)

    def test_profile_str(self):
        self.assertEqual(str(self.profile), f"Profile de {self.user.username}")

class HistoriqueModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.historique = Historique.objects.create(
            user=self.user,
            content_type='course',
            content_id=1,
            progress=50
        )

    def test_historique_creation(self):
        self.assertEqual(self.historique.user, self.user)
        self.assertEqual(self.historique.content_type, 'course')
        self.assertEqual(self.historique.content_id, 1)
        self.assertEqual(self.historique.progress, 50)
        self.assertFalse(self.historique.completed)

    def test_historique_str(self):
        self.assertEqual(str(self.historique), f"{self.user.username} - course #1")

    def test_unique_together(self):
        # Test that unique_together constraint works
        with self.assertRaises(Exception):
            Historique.objects.create(
                user=self.user,
                content_type='course',
                content_id=1,
                progress=75
            )
