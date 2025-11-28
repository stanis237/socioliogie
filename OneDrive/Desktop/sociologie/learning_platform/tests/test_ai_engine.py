"""
Tests pour les recommandations IA
"""
import pytest
from ai_module.ai_engine import RecommendationEngine


class TestRecommendationEngine:
    
    def setup_method(self):
        """Initialiser le moteur"""
        self.engine = RecommendationEngine()
    
    def test_build_user_profile(self):
        """Test la construction du profil utilisateur"""
        # Mock user
        user = type('User', (), {
            'id': '123',
            'learning_style': 'visual',
            'proficiency_level': 'intermediate',
            'interests': ['math', 'science'],
            'goals': ['learn python']
        })()
        
        # Mock analytics
        analytics = type('Analytics', (), {
            'total_learning_time': 100,
            'average_exercise_score': 75.5,
            'learning_consistency': 80,
            'motivation_level': 70
        })()
        
        profile = self.engine.build_user_profile(user, analytics, [])
        
        assert profile['user_id'] == '123'
        assert profile['learning_style'] == 'visual'
        assert profile['interests'] == ['math', 'science']
    
    def test_calculate_interest_match(self):
        """Test le calcul du matching des intérêts"""
        user_interests = ['python', 'ai', 'machine learning']
        course_tags = ['python', 'ai', 'data science']
        
        score = self.engine._calculate_interest_match(user_interests, course_tags)
        
        assert 0 <= score <= 1
        assert score > 0  # Il y a des intérêts communs
    
    def test_calculate_difficulty_match(self):
        """Test le matching de difficulté"""
        scores = [
            ('beginner', 'beginner', 1.0),
            ('beginner', 'intermediate', 0.75),
            ('intermediate', 'advanced', 0.75),
            ('beginner', 'expert', 0.5),
        ]
        
        for user_level, course_level, expected_min in scores:
            score = self.engine._calculate_difficulty_match(user_level, course_level)
            assert score >= expected_min - 0.01  # Toleranza
