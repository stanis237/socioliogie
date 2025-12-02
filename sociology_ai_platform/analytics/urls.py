from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('recommendations/generate/', views.generate_ai_recommendations, name='generate_ai_recommendations'),
    path('emotion/record/', views.record_emotion, name='record_emotion'),
    path('emotion/recognize/', views.emotion_recognition, name='emotion_recognition'),
    path('emotion/api/recognize/', views.recognize_emotion_api, name='recognize_emotion_api'),
]
