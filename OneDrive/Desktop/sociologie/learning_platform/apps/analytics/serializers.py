from rest_framework import serializers
from .models import UserAnalytics, CourseAnalytics, LearningPath, DailyMetric, PerformanceMetric

class UserAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnalytics
        fields = ['total_learning_time', 'total_courses_enrolled', 'total_courses_completed',
                 'total_exercises_attempted', 'total_exercises_passed', 'average_exercise_score',
                 'current_streak', 'longest_streak', 'learning_consistency', 'motivation_level']
        read_only_fields = '__all__'


class CourseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAnalytics
        fields = ['course', 'total_enrollments', 'completed_count', 'completion_rate',
                 'average_score', 'average_time_spent', 'dropout_rate']
        read_only_fields = '__all__'


class LearningPathSerializer(serializers.ModelSerializer):
    courses_titles = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningPath
        fields = ['id', 'name', 'description', 'courses', 'courses_titles', 'total_duration_hours',
                 'estimated_completion_date', 'is_active', 'created_at']
        read_only_fields = ['created_at']
    
    def get_courses_titles(self, obj):
        return [course.title for course in obj.courses.all()]


class DailyMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyMetric
        fields = ['date', 'learning_time_minutes', 'exercises_attempted', 'exercises_passed',
                 'videos_watched', 'pages_read', 'mood_score', 'motivation_score']
        read_only_fields = ['date']


class PerformanceMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceMetric
        fields = ['subject', 'category', 'total_attempts', 'successful_attempts', 'success_rate',
                 'average_score', 'difficulty_rating', 'last_attempted']
        read_only_fields = '__all__'
