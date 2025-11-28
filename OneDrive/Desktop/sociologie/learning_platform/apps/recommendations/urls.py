from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentRecommendationViewSet, ExerciseRecommendationViewSet

router = DefaultRouter()
router.register(r'content', ContentRecommendationViewSet, basename='content-recommendations')
router.register(r'exercises', ExerciseRecommendationViewSet, basename='exercise-recommendations')

urlpatterns = [
    path('', include(router.urls)),
]
