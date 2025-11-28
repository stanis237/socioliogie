from django.contrib import admin
from .models import UserAnalytics, CourseAnalytics, LearningPath, DailyMetric, PerformanceMetric

@admin.register(UserAnalytics)
class UserAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_learning_time', 'total_courses_completed', 'current_streak']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CourseAnalytics)
class CourseAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['course', 'total_enrollments', 'completion_rate', 'average_score']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'total_duration_hours', 'is_active']
    filter_horizontal = ['courses']

@admin.register(DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'learning_time_minutes', 'exercises_passed']
    list_filter = ['date']
    date_hierarchy = 'date'

@admin.register(PerformanceMetric)
class PerformanceMetricAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'success_rate', 'average_score']
    list_filter = ['category']
