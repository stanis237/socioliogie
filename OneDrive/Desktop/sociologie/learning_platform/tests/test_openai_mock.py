from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from apps.content.models import Course
from apps.recommendations.models import ContentRecommendation, AIExplainability
from ai_module.services import RecommendationService

User = get_user_model()


class OpenAIIntegrationMockTests(TestCase):
    """Tests that mock OpenAI explanation generation and verify saved explanations."""

    def setUp(self):
        self.user = User.objects.create_user(email='tester@example.com', password='password123')
        self.course = Course.objects.create(title='Mock Course', description='Desc', category='misc')

    @patch('ai_module.services.openai_service.generate_explanation')
    def test_save_recommendations_uses_openai_explanation(self, mock_generate):
        # Arrange
        mock_generate.return_value = 'Explication générée par OpenAI.'

        rec = {
            'course': self.course.id,
            'reason': 'performance',
            'reason_text': 'Texte original fourni',
            'score': 0.85,
            'factors': [{'name': 'perf', 'weight': 0.7, 'explanation': 'Basé sur vos résultats récents'}]
        }

        # Act
        RecommendationService.save_recommendations(self.user, [rec])

        # Assert
        content_recs = ContentRecommendation.objects.filter(user=self.user)
        self.assertEqual(content_recs.count(), 1)
        content = content_recs.first()
        self.assertEqual(content.reason_explanation, 'Explication générée par OpenAI.')

        ai_expl = AIExplainability.objects.get(recommendation=content)
        self.assertEqual(ai_expl.user_friendly_explanation, 'Explication générée par OpenAI.')

    @patch('ai_module.services.openai_service.generate_explanation')
    def test_save_recommendations_fallback_when_openai_returns_none(self, mock_generate):
        # Arrange
        mock_generate.return_value = None

        rec = {
            'course': self.course.id,
            'reason': 'learning_style',
            'reason_text': 'Explication fournie par l\'algorithme',
            'score': 0.6,
            'factors': []
        }

        # Act
        RecommendationService.save_recommendations(self.user, [rec])

        # Assert
        content_recs = ContentRecommendation.objects.filter(user=self.user)
        self.assertEqual(content_recs.count(), 1)
        content = content_recs.first()
        # Should fallback to provided reason_text
        self.assertEqual(content.reason_explanation, 'Explication fournie par l\'algorithme')

        ai_expl = AIExplainability.objects.get(recommendation=content)
        self.assertEqual(ai_expl.user_friendly_explanation, 'Explication fournie par l\'algorithme')

    @patch('ai_module.services.openai_service.generate_explanation')
    def test_save_recommendations_handles_exception_from_openai(self, mock_generate):
        # Arrange: OpenAI raises an exception
        mock_generate.side_effect = Exception('OpenAI failure')

        rec = {
            'course': self.course.id,
            'reason': 'trend',
            'reason_text': 'Explication par défaut',
            'score': 0.5,
            'factors': []
        }

        # Act: should not raise, service should handle exception and fallback
        RecommendationService.save_recommendations(self.user, [rec])

        # Assert
        content_recs = ContentRecommendation.objects.filter(user=self.user)
        self.assertEqual(content_recs.count(), 1)
        content = content_recs.first()
        # Fallback to provided reason_text
        self.assertEqual(content.reason_explanation, 'Explication par défaut')

        ai_expl = AIExplainability.objects.get(recommendation=content)
        self.assertEqual(ai_expl.user_friendly_explanation, 'Explication par défaut')
