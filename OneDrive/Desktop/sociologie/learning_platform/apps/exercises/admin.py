from django.contrib import admin
from .models import Exercise, Question, Answer, ExerciseSubmission, QuestionResponse, Quiz

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'exercise_type', 'difficulty_level', 'points']
    list_filter = ['exercise_type', 'difficulty_level', 'adaptive']
    search_fields = ['title']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'question_type', 'difficulty_score']
    list_filter = ['question_type']
    search_fields = ['text']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct', 'question']
    list_filter = ['is_correct']

@admin.register(ExerciseSubmission)
class ExerciseSubmissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'status', 'score', 'percentage', 'submitted_at']
    list_filter = ['status', 'submitted_at']
    search_fields = ['user__username', 'exercise__title']
    readonly_fields = ['started_at', 'submitted_at', 'completed_at']

@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ['submission', 'question', 'is_correct', 'score']
    list_filter = ['is_correct']

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'pass_percentage', 'max_attempts']
    list_filter = ['pass_percentage']
    search_fields = ['title']
