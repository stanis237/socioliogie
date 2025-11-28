from django.contrib import admin
from .models import ContentRecommendation, ExerciseRecommendation, RecommendationLog, AIExplainability

@admin.register(ContentRecommendation)
class ContentRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommended_course', 'reason', 'confidence_score', 'is_clicked']
    list_filter = ['reason', 'is_clicked', 'is_completed']
    search_fields = ['user__username']

@admin.register(ExerciseRecommendation)
class ExerciseRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'difficulty_adjusted', 'expected_performance', 'is_attempted']
    list_filter = ['difficulty_adjusted', 'is_attempted']

@admin.register(RecommendationLog)
class RecommendationLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'algorithm_version', 'user_clicked', 'user_feedback', 'created_at']
    list_filter = ['user_feedback', 'created_at']
    date_hierarchy = 'created_at'

@admin.register(AIExplainability)
class AIExplainabilityAdmin(admin.ModelAdmin):
    list_display = ['recommendation', 'primary_factor', 'primary_factor_contribution']
    readonly_fields = ['created_at']
