from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserAnalyticsViewSet, CourseAnalyticsViewSet, LearningPathViewSet,
    DailyMetricViewSet, PerformanceMetricViewSet
)

router = DefaultRouter()
router.register(r'user', UserAnalyticsViewSet, basename='user-analytics')
router.register(r'courses', CourseAnalyticsViewSet, basename='course-analytics')
router.register(r'learning-paths', LearningPathViewSet, basename='learning-paths')
router.register(r'daily-metrics', DailyMetricViewSet, basename='daily-metrics')
router.register(r'performance', PerformanceMetricViewSet, basename='performance')

urlpatterns = [
    path('', include(router.urls)),
]
