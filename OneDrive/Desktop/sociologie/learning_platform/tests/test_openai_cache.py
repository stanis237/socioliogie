from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from unittest.mock import patch
from apps.content.models import Course
from apps.recommendations.models import ContentRecommendation, AIExplainability
from ai_module.services import RecommendationService

User = get_user_model()


class OpenAICacheTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='cachetester@example.com', password='password123')
        self.course = Course.objects.create(title='Cache Course', description='Desc', category='misc')

    @patch('ai_module.services.openai_service.generate_explanation')
    @patch('ai_module.services.cache.get')
    def test_save_recommendations_uses_cached_explanation(self, mock_cache_get, mock_generate):
        # Simulate a cached explanation being present
        mock_cache_get.return_value = 'Explication mise en cache'
        mock_generate.return_value = 'NEVER_CALLED'

        rec = {
            'course': self.course.id,
            'reason': 'performance',
            'reason_text': 'Texte original',
            'score': 0.9,
            'factors': []
        }

        RecommendationService.save_recommendations(self.user, [rec])

        content = ContentRecommendation.objects.filter(user=self.user).first()
        self.assertIsNotNone(content)
        self.assertEqual(content.reason_explanation, 'Explication mise en cache')
        # Ensure OpenAI was not called when cache provided the value
        mock_generate.assert_not_called()

    @override_settings(OPENAI_CACHE_ENABLED=True, OPENAI_EXPLANATION_TTL=3600)
    @patch('ai_module.services.cache.set')
    @patch('ai_module.services.cache.get')
    @patch('ai_module.services.openai_service.generate_explanation')
    def test_save_recommendations_sets_cache_when_openai_returns(self, mock_generate, mock_cache_get, mock_cache_set):
        # No cache present initially
        mock_cache_get.return_value = None
        mock_generate.return_value = 'Explication générée par OpenAI et mise en cache'

        rec = {
            'course': self.course.id,
            'reason': 'performance',
            'reason_text': 'Texte original',
            'score': 0.75,
            'factors': []
        }

        RecommendationService.save_recommendations(self.user, [rec])

        content = ContentRecommendation.objects.filter(user=self.user).first()
        self.assertIsNotNone(content)
        self.assertEqual(content.reason_explanation, 'Explication générée par OpenAI et mise en cache')

        ai_expl = AIExplainability.objects.get(recommendation=content)
        self.assertEqual(ai_expl.user_friendly_explanation, 'Explication générée par OpenAI et mise en cache')

        # Ensure cache.set was called to save the new explanation
        self.assertTrue(mock_cache_set.called)
