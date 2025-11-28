from django.contrib import admin
from .models import Course, Module, Lesson, Resource, EnrolledCourse

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'difficulty_level', 'status', 'students_enrolled', 'rating']
    list_filter = ['status', 'category', 'difficulty_level']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'slug', 'description', 'summary', 'category', 'tags')
        }),
        ('Contenu', {
            'fields': ('instructor', 'cover_image', 'video_intro', 'duration_hours', 'difficulty_level')
        }),
        ('Structure', {
            'fields': ('prerequisites', 'learning_outcomes')
        }),
        ('Métriques', {
            'fields': ('students_enrolled', 'rating', 'reviews_count')
        }),
        ('Statut', {
            'fields': ('status', 'published_at', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['published_at', 'created_at', 'updated_at']

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes']
    list_filter = ['course']
    search_fields = ['title']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'content_type', 'difficulty_level', 'is_published']
    list_filter = ['content_type', 'difficulty_level', 'is_published']
    search_fields = ['title']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'resource_type']
    list_filter = ['resource_type']

@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'progress_percentage', 'enrolled_at', 'completed_at']
    list_filter = ['enrolled_at']
    search_fields = ['user__username', 'course__title']
