from django.contrib import admin
from .models import EmotionDetection, EmotionalState, EmotionAdaptation, EmotionFeedback, EmotionalTrend

@admin.register(EmotionDetection)
class EmotionDetectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'detected_emotion', 'confidence', 'activity_context', 'created_at']
    list_filter = ['detected_emotion', 'confidence']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'anonymized_image_hash']

@admin.register(EmotionalState)
class EmotionalStateAdmin(admin.ModelAdmin):
    list_display = ['user', 'average_emotion', 'stress_level', 'engagement_level']
    readonly_fields = ['last_updated']

@admin.register(EmotionAdaptation)
class EmotionAdaptationAdmin(admin.ModelAdmin):
    list_display = ['user', 'adaptation_type', 'user_accepted', 'effectiveness']
    list_filter = ['adaptation_type', 'user_accepted']

@admin.register(EmotionFeedback)
class EmotionFeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_accurate', 'rating', 'created_at']
    list_filter = ['is_accurate', 'rating']

@admin.register(EmotionalTrend)
class EmotionalTrendAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'dominant_emotion', 'correlation_with_performance']
    list_filter = ['dominant_emotion', 'date']
    date_hierarchy = 'date'
