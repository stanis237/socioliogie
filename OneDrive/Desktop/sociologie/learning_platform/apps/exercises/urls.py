from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ExerciseSubmissionViewSet, QuizViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet, basename='exercises')
router.register(r'submissions', ExerciseSubmissionViewSet, basename='submissions')
router.register(r'quizzes', QuizViewSet, basename='quizzes')

urlpatterns = [
    path('', include(router.urls)),
]
