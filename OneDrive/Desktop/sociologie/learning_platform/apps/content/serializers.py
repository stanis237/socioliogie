from rest_framework import serializers
from .models import Course, Module, Lesson, Resource, EnrolledCourse

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'resource_type', 'file', 'url', 'created_at']
        read_only_fields = ['created_at']


class LessonSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'module', 'title', 'content_type', 'description', 'order', 'duration_minutes',
                 'text_content', 'video_url', 'document_file', 'learning_objectives', 'keywords',
                 'difficulty_level', 'is_published', 'resources', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Module
        fields = ['id', 'course', 'title', 'description', 'order', 'duration_minutes',
                 'is_locked', 'lessons', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'summary', 'difficulty_level', 'category',
                 'cover_image', 'duration_hours', 'students_enrolled', 'rating', 'instructor']


class CourseDetailSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'difficulty_level', 'category', 'tags',
                 'instructor', 'cover_image', 'video_intro', 'duration_hours', 'prerequisites',
                 'learning_outcomes', 'students_enrolled', 'rating', 'reviews_count', 'status',
                 'modules', 'created_at', 'updated_at', 'published_at']
        read_only_fields = ['created_at', 'updated_at', 'published_at']


class EnrolledCourseSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    
    class Meta:
        model = EnrolledCourse
        fields = ['id', 'user', 'course', 'enrolled_at', 'completed_at', 'progress_percentage',
                 'lessons_completed', 'current_module', 'last_accessed', 'notes']
        read_only_fields = ['id', 'enrolled_at', 'completed_at', 'user']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrolledCourse
        fields = ['course']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
