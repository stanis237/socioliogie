from django.contrib import admin
from .models import Notification, NotificationPreference, EmailTemplate, NotificationSchedule, NotificationLog

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'channel', 'is_read', 'created_at']
    list_filter = ['notification_type', 'channel', 'is_read']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at', 'read_at', 'clicked_at']

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'enable_email', 'enable_push', 'email_frequency']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    search_fields = ['name', 'code']

@admin.register(NotificationSchedule)
class NotificationScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'frequency', 'is_active', 'start_date']
    list_filter = ['frequency', 'is_active']

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['notification', 'channel', 'status', 'sent_at']
    list_filter = ['channel', 'status', 'sent_at']
    date_hierarchy = 'sent_at'
