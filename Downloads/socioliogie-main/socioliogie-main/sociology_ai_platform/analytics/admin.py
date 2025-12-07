from django.contrib import admin
from .models import Recommendation, EmotionData

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'score', 'viewed', 'created_at']
    list_filter = ['viewed', 'created_at']
    search_fields = ['user__username', 'course__title']

@admin.register(EmotionData)
class EmotionDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'emotion_type', 'intensity', 'context', 'recorded_at']
    list_filter = ['emotion_type', 'recorded_at']
    search_fields = ['user__username', 'context']
