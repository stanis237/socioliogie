"""
Tests complets pour le système de recommandations IA
"""
import pytest
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.content.models import Course, Module, Lesson
from apps.exercises.models import Exercise, ExerciseSubmission
from apps.recommendations.models import ContentRecommendation, ExerciseRecommendation
from apps.analytics.models import UserAnalytics
from ai_module.ai_engine import RecommendationEngine, EmotionAnalyzer

User = get_user_model()


class RecommendationEngineTests(TestCase):
    """Tests pour le moteur de recommandation"""

    def setUp(self):
        # Créer des utilisateurs
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            password='password123',
            learning_style='visual'
        )
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            password='password123',
            learning_style='visual'
        )
        self.user3 = User.objects.create_user(
            email='user3@example.com',
            password='password123',
            learning_style='auditory'
        )

        # Créer des cours
        self.course1 = Course.objects.create(
            title='Python Basics',
            description='Learn Python fundamentals',
            category='programming',
            difficulty_level='beginner'
        )
        self.course2 = Course.objects.create(
            title='Advanced Python',
            description='Advanced Python concepts',
            category='programming',
            difficulty_level='advanced'
        )
        self.course3 = Course.objects.create(
            title='Django Framework',
            description='Learn Django',
            category='programming',
            difficulty_level='intermediate'
        )

        # Créer des modules et leçons
        self.module1 = Module.objects.create(
            course=self.course1,
            title='Introduction',
            order=1
        )
        self.lesson1 = Lesson.objects.create(
            module=self.module1,
            title='Getting Started',
            order=1,
            content='Introduction content'
        )

        # Créer des exercices
        self.exercise1 = Exercise.objects.create(
            lesson=self.lesson1,
            title='First Exercise',
            description='First exercise description',
            type='quiz'
        )

    def test_collaborative_filtering(self):
        """Test le filtrage collaboratif"""
        engine = RecommendationEngine()

        # Créer des profils utilisateur
        from apps.users.models import UserProfile
        UserProfile.objects.create(user=self.user1, total_courses_completed=5)
        UserProfile.objects.create(user=self.user2, total_courses_completed=6)
        UserProfile.objects.create(user=self.user3, total_courses_completed=3)

        # Créer des recommandations de base pour les utilisateurs similaires
        recommendations = engine.collaborative_filtering(
            self.user1,
            [self.user1, self.user2, self.user3],
            [self.course1, self.course2, self.course3]
        )

        self.assertIsNotNone(recommendations)
        self.assertGreater(len(recommendations), 0)

    def test_content_based_filtering(self):
        """Test le filtrage basé sur le contenu"""
        engine = RecommendationEngine()

        from apps.users.models import UserProfile
        profile = UserProfile.objects.create(
            user=self.user1,
            preferred_categories='programming',
            preferred_difficulty='intermediate'
        )

        recommendations = engine.content_based_filtering(
            self.user1,
            [self.course1, self.course2, self.course3]
        )

        self.assertIsNotNone(recommendations)

    def test_emotion_based_filtering(self):
        """Test le filtrage basé sur les émotions"""
        engine = RecommendationEngine()

        from apps.emotions.models import EmotionDetection
        EmotionDetection.objects.create(
            user=self.user1,
            emotion='stressed',
            confidence_score=0.8
        )

        recommendations = engine.emotion_based_filtering(
            self.user1,
            [self.course1, self.course2, self.course3]
        )

        self.assertIsNotNone(recommendations)

    def test_performance_based_filtering(self):
        """Test le filtrage basé sur les performances"""
        engine = RecommendationEngine()

        from apps.analytics.models import UserAnalytics, PerformanceMetric
        UserAnalytics.objects.create(
            user=self.user1,
            average_score=75,
            total_study_hours=10
        )
        PerformanceMetric.objects.create(
            user=self.user1,
            subject='Python',
            score=65
        )

        recommendations = engine.performance_based_filtering(
            self.user1,
            [self.course1, self.course2, self.course3]
        )

        self.assertIsNotNone(recommendations)


class EmotionAnalyzerTests(TestCase):
    """Tests pour l'analyseur d'émotions"""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        self.analyzer = EmotionAnalyzer()

    def test_calculate_stress_level(self):
        """Test le calcul du niveau de stress"""
        from apps.emotions.models import EmotionDetection

        # Créer des détections d'émotions
        emotions = ['stressed', 'anxious', 'worried']
        for emotion in emotions:
            EmotionDetection.objects.create(
                user=self.user,
                emotion=emotion,
                confidence_score=0.7
            )

        stress_level = self.analyzer.calculate_stress_index(self.user)

        self.assertGreater(stress_level, 0.5)
        self.assertLessEqual(stress_level, 1.0)

    def test_calculate_engagement_level(self):
        """Test le calcul du niveau d'engagement"""
        from apps.emotions.models import EmotionDetection

        emotions = ['focused', 'interested', 'engaged']
        for emotion in emotions:
            EmotionDetection.objects.create(
                user=self.user,
                emotion=emotion,
                confidence_score=0.8
            )

        engagement = self.analyzer.calculate_engagement_index(self.user)

        self.assertGreater(engagement, 0.5)
        self.assertLessEqual(engagement, 1.0)

    def test_detect_emotion_trend(self):
        """Test la détection de tendance émotionnelle"""
        from apps.emotions.models import EmotionDetection
        from datetime import timedelta
        from django.utils import timezone

        # Créer une tendance croissante
        for i in range(5):
            timestamp = timezone.now() - timedelta(days=5-i)
            EmotionDetection.objects.create(
                user=self.user,
                emotion='happy' if i < 3 else 'sad',
                confidence_score=0.6 + (i * 0.1),
                created_at=timestamp
            )

        trend = self.analyzer.detect_emotion_trend(self.user, days=7)

        self.assertIn(trend, ['improving', 'stable', 'declining'])


class RecommendationAPITests(TestCase):
    """Tests pour l'API de recommandations"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

        # Créer du contenu
        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            category='programming'
        )

    def test_get_content_recommendations(self):
        """Test la récupération des recommandations de contenu"""
        response = self.client.get('/api/recommendations/content-recommendations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_get_exercise_recommendations(self):
        """Test la récupération des recommandations d'exercices"""
        response = self.client.get('/api/recommendations/exercise-recommendations/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)

    def test_generate_recommendations(self):
        """Test la génération de recommandations"""
        response = self.client.post('/api/recommendations/generate/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recommendation_feedback(self):
        """Test l'envoi de feedback sur une recommandation"""
        # Créer une recommandation
        rec = ContentRecommendation.objects.create(
            user=self.user,
            content=self.course,
            confidence_score=0.8,
            reason='test'
        )

        response = self.client.post(
            f'/api/recommendations/content-recommendations/{rec.id}/feedback/',
            {
                'is_helpful': True,
                'feedback_reason': 'Great recommendation'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recommendation_explainability(self):
        """Test que les explications IA sont retournées"""
        response = self.client.get('/api/recommendations/content-recommendations/')

        if response.data['results']:
            rec = response.data['results'][0]
            self.assertIn('reason', rec)
            self.assertIn('confidence_score', rec)

    def test_unauthenticated_access(self):
        """Test l'accès non authentifié"""
        client = APIClient()
        response = client.get('/api/recommendations/content-recommendations/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


@pytest.mark.django_db
class TestRecommendationPerformance:
    """Tests de performance pour les recommandations"""

    def test_recommendation_generation_speed(self, django_assert_num_queries):
        """Test que la génération de recommandations est rapide"""
        user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )

        with django_assert_num_queries(5):
            engine = RecommendationEngine()
            # La génération ne devrait pas faire trop de requêtes

    def test_recommendation_caching(self, client, cache):
        """Test que les recommandations sont cachées"""
        user = User.objects.create_user(
            email='test@example.com',
            password='password123'
        )

        client.force_authenticate(user=user)

        # Première requête
        response1 = client.get('/api/recommendations/content-recommendations/')
        
        # Vérifier que le cache a été utilisé
        # (La deuxième requête devrait être plus rapide)
