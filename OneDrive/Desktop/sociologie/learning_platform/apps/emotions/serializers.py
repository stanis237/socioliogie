from rest_framework import serializers
from .models import EmotionDetection, EmotionalState, EmotionAdaptation, EmotionFeedback, EmotionalTrend

class EmotionDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionDetection
        fields = ['id', 'detected_emotion', 'confidence', 'emotion_scores', 'activity_context',
                 'recommended_action', 'created_at']
        read_only_fields = ['id', 'created_at']


class EmotionalStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionalState
        # expose all fields but mark them read-only (aggregated data)
        fields = '__all__'
        read_only_fields = tuple([f.name for f in EmotionalState._meta.fields])


class EmotionAdaptationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionAdaptation
        fields = ['id', 'adaptation_type', 'description', 'message_to_user', 'new_difficulty',
                 'new_content_type', 'user_accepted', 'effectiveness', 'created_at']
        # keep id and created_at read-only; description/message_to_user should be writable
        # because they are required fields on the model when creating adaptations.
        read_only_fields = ['id', 'created_at']


class EmotionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionFeedback
        fields = ['id', 'emotion_detection', 'is_accurate', 'actual_emotion', 'comments', 'rating']
        read_only_fields = ['id']


class EmotionalTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionalTrend
        fields = '__all__'
        read_only_fields = tuple([f.name for f in EmotionalTrend._meta.fields])
