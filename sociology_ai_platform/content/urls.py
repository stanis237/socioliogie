from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('generate/', views.generate_course, name='generate_course'),
    path('generate/api/', views.generate_course_api, name='generate_course_api'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('exercise/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
]
