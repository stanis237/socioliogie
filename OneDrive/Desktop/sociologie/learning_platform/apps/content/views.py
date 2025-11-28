from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Course, Module, Lesson, Resource, EnrolledCourse
from .serializers import (
    CourseListSerializer, CourseDetailSerializer, ModuleSerializer,
    LessonSerializer, ResourceSerializer, EnrolledCourseSerializer,
    EnrollmentSerializer
)

class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet pour la gestion des cours"""
    queryset = Course.objects.filter(status='published')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['difficulty_level', 'category', 'status']
    search_fields = ['title', 'description', 'instructor', 'category']
    ordering_fields = ['created_at', 'rating', 'students_enrolled']
    ordering = ['-published_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseListSerializer
    
    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """Récupérer les cours de l'utilisateur"""
        enrolled = EnrolledCourse.objects.filter(user=request.user).select_related('course')
        serializer = EnrolledCourseSerializer(enrolled, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """S'inscrire à un cours"""
        course = self.get_object()
        enrolled, created = EnrolledCourse.objects.get_or_create(
            user=request.user,
            course=course
        )
        if created:
            course.students_enrolled += 1
            course.save()
            return Response(
                {'message': 'Inscription réussie'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'message': 'Déjà inscrit à ce cours'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def unenroll(self, request, pk=None):
        """Se désinscrire d'un cours"""
        course = self.get_object()
        enrolled = EnrolledCourse.objects.filter(user=request.user, course=course)
        if enrolled.exists():
            enrolled.delete()
            course.students_enrolled -= 1
            course.save()
            return Response({'message': 'Désinscription réussie'})
        return Response({'error': 'Pas inscrit à ce cours'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Récupérer la progression dans le cours"""
        course = self.get_object()
        try:
            enrolled = EnrolledCourse.objects.get(user=request.user, course=course)
            serializer = EnrolledCourseSerializer(enrolled)
            return Response(serializer.data)
        except EnrolledCourse.DoesNotExist:
            return Response({'error': 'Pas inscrit'}, status=status.HTTP_404_NOT_FOUND)


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les modules"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        course_id = self.request.query_params.get('course_id')
        if course_id:
            return Module.objects.filter(course_id=course_id)
        return Module.objects.all()


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les leçons"""
    queryset = Lesson.objects.filter(is_published=True)
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        module_id = self.request.query_params.get('module_id')
        if module_id:
            return Lesson.objects.filter(module_id=module_id, is_published=True)
        return Lesson.objects.filter(is_published=True)


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet pour consulter les ressources"""
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        lesson_id = self.request.query_params.get('lesson_id')
        if lesson_id:
            return Resource.objects.filter(lesson_id=lesson_id)
        return Resource.objects.all()
