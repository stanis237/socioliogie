from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, UserProfile, UserSettings, UserActivityLog


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin for CustomUser based on Django's built-in UserAdmin.

    This ensures the admin has proper create/edit UX and permission handling
    while exposing the custom profile fields.
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'learning_style', 'proficiency_level', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'learning_style', 'proficiency_level')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ('id', 'created_at', 'updated_at', 'last_activity')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'bio')}),
        (_('Preferences & Progress'), {'fields': ('learning_style', 'proficiency_level', 'interests', 'goals', 'daily_goal_minutes', 'timezone')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_activity', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_learning_minutes', 'exercises_completed', 'average_score')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'language', 'notifications_email')


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username',)
    readonly_fields = ('timestamp',)
