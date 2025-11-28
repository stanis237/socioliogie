from rest_framework import serializers
from .models import ContentRecommendation, ExerciseRecommendation, AIExplainability


class AIExplainabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIExplainability
        fields = ['id', 'recommendation', 'factors', 'primary_factor', 'primary_factor_contribution',
                 'user_friendly_explanation', 'supporting_data', 'alternative_recommendations',
                 'created_at']
        read_only_fields = ['created_at']


class ContentRecommendationSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='recommended_course.title', read_only=True)
    lesson_title = serializers.CharField(source='recommended_lesson.title', read_only=True)
    explanation = AIExplainabilitySerializer(source='explanation', read_only=True)

    class Meta:
        model = ContentRecommendation
        fields = ['id', 'recommended_course', 'course_title', 'recommended_lesson', 'lesson_title',
             'reason', 'reason_explanation', 'confidence_score', 'priority', 'is_clicked',
             'is_completed', 'dismissed', 'explanation', 'created_at']
        read_only_fields = ['created_at']


class ExerciseRecommendationSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)

    class Meta:
        model = ExerciseRecommendation
        fields = ['id', 'exercise', 'exercise_title', 'difficulty_adjusted', 'expected_performance',
                 'reason', 'is_attempted', 'is_passed', 'actual_score', 'created_at']
        read_only_fields = ['created_at']
