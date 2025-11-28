from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Exercise(models.Model):
    """
    Modèle pour les exercices
    """
    DIFFICULTY_LEVELS = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
    ]
    
    EXERCISE_TYPES = [
        ('quiz', 'Quiz'),
        ('coding', 'Code'),
        ('matching', 'Appariement'),
        ('essay', 'Essai'),
        ('fill_blank', 'Compléter'),
        ('multiple_choice', 'Choix multiples'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey('content.Lesson', on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    description = models.TextField()
    exercise_type = models.CharField(max_length=50, choices=EXERCISE_TYPES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='medium')
    
    instructions = models.TextField()
    points = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    time_limit_minutes = models.IntegerField(null=True, blank=True)
    
    learning_objectives = models.JSONField(default=list)
    keywords = models.JSONField(default=list)
    
    # Configuration adaptative
    adaptive = models.BooleanField(default=False, help_text="Exercice adaptatif par IA")
    adjust_difficulty = models.BooleanField(default=False, help_text="Ajuster la difficulté automatiquement")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Exercice"
        verbose_name_plural = "Exercices"
        ordering = ['lesson', '-created_at']
    
    def __str__(self):
        return self.title


class Question(models.Model):
    """
    Modèle pour les questions
    """
    QUESTION_TYPES = [
        ('multiple_choice', 'Choix multiples'),
        ('true_false', 'Vrai/Faux'),
        ('short_answer', 'Réponse courte'),
        ('essay', 'Essai'),
        ('coding', 'Code'),
        ('fill_blank', 'Compléter'),
        ('matching', 'Appariement'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)
    order = models.IntegerField()
    text = models.TextField()
    explanation = models.TextField(blank=True, help_text="Explication de la réponse correcte")
    image = models.ImageField(upload_to='questions/', blank=True)
    
    hints = models.JSONField(default=list)
    difficulty_score = models.FloatField(default=0.5, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['exercise', 'order']
        unique_together = ('exercise', 'order')
    
    def __str__(self):
        return f"{self.exercise.title} - Q{self.order}"


class Answer(models.Model):
    """
    Modèle pour les réponses possibles aux questions
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    order = models.IntegerField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(blank=True)
    feedback = models.TextField(blank=True, help_text="Feedback pour cette réponse")
    
    class Meta:
        verbose_name = "Réponse"
        verbose_name_plural = "Réponses"
        ordering = ['question', 'order']
        unique_together = ('question', 'order')
    
    def __str__(self):
        return f"{self.question.text[:50]} - {self.text[:50]}"


class ExerciseSubmission(models.Model):
    """
    Soumission d'exercice par un utilisateur
    """
    SUBMISSION_STATUS = [
        ('pending', 'En attente'),
        ('submitted', 'Soumis'),
        ('graded', 'Évalué'),
        ('reviewed', 'Revu'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='exercise_submissions')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    
    status = models.CharField(max_length=20, choices=SUBMISSION_STATUS, default='pending')
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent_seconds = models.IntegerField(default=0)
    
    score = models.IntegerField(null=True, blank=True)
    max_score = models.IntegerField()
    percentage = models.FloatField(null=True, blank=True)
    
    feedback = models.TextField(blank=True)
    ai_feedback = models.TextField(blank=True, help_text="Feedback généré par IA")
    
    attempts_count = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Soumission d'exercice"
        verbose_name_plural = "Soumissions d'exercice"
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['user', 'exercise']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"


class QuestionResponse(models.Model):
    """
    Réponse de l'utilisateur à une question spécifique
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(ExerciseSubmission, on_delete=models.CASCADE, related_name='question_responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True, blank=True)
    text_response = models.TextField(blank=True)
    code_response = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    time_spent_seconds = models.IntegerField(default=0)
    attempt_number = models.IntegerField(default=1)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Réponse à une question"
        verbose_name_plural = "Réponses aux questions"
        ordering = ['submission', 'question__order']
    
    def __str__(self):
        return f"{self.submission.user.username} - Q{self.question.order}"


class Quiz(models.Model):
    """
    Quiz spécifiques (différent des exercices)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey('content.Lesson', on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question)
    
    pass_percentage = models.FloatField(default=70.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    randomize_questions = models.BooleanField(default=False)
    randomize_answers = models.BooleanField(default=False)
    shuffle_mode = models.BooleanField(default=False)
    show_answers = models.BooleanField(default=True)
    allow_review = models.BooleanField(default=True)
    max_attempts = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"
    
    def __str__(self):
        return self.title
