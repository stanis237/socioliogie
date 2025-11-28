from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmotionDetectionViewSet, EmotionalStateViewSet, EmotionAdaptationViewSet,
    EmotionFeedbackViewSet, EmotionalTrendViewSet
)

router = DefaultRouter()
router.register(r'detections', EmotionDetectionViewSet, basename='detections')
router.register(r'state', EmotionalStateViewSet, basename='state')
router.register(r'adaptations', EmotionAdaptationViewSet, basename='adaptations')
router.register(r'feedback', EmotionFeedbackViewSet, basename='feedback')
router.register(r'trends', EmotionalTrendViewSet, basename='trends')

urlpatterns = [
    path('', include(router.urls)),
]
