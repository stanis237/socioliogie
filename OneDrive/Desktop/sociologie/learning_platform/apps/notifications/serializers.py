from rest_framework import serializers
from .models import Notification, NotificationPreference, EmailTemplate, NotificationSchedule

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'channel', 'priority',
                 'is_read', 'clicked', 'read_at', 'clicked_at', 'action_url', 'created_at']
        read_only_fields = ['id', 'created_at', 'read_at', 'clicked_at']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['enable_email', 'enable_push', 'enable_in_app', 'enable_sms',
                 'enable_reminders', 'enable_achievements', 'enable_recommendations',
                 'enable_messages', 'enable_alerts', 'enable_encouragement',
                 'quiet_hours_enabled', 'quiet_hours_start', 'quiet_hours_end',
                 'email_frequency', 'allow_personalization', 'allow_emotional_adaptation']


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'name', 'code', 'description', 'subject', 'is_active']
        read_only_fields = ['html_content', 'text_content']


class NotificationScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSchedule
        fields = ['id', 'title', 'message', 'notification_type', 'frequency', 'start_date',
                 'end_date', 'time', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                 'saturday', 'sunday', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
