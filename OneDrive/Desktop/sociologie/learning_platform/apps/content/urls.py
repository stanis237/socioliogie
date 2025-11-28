from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, ModuleViewSet, LessonViewSet, ResourceViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'modules', ModuleViewSet, basename='modules')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'resources', ResourceViewSet, basename='resources')

urlpatterns = [
    path('', include(router.urls)),
]
