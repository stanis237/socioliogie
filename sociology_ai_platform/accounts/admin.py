from django.contrib import admin
from .models import UserProfile, Historique

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'points', 'created_at']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Historique)
class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'content_id', 'progress', 'completed', 'last_accessed']
    list_filter = ['content_type', 'completed', 'last_accessed']
    search_fields = ['user__username']
