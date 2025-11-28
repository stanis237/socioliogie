from django.db import models
import uuid

class UserAnalytics(models.Model):
    """
    Analyse des activités utilisateur
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='analytics')
    
    # Statistiques générales
    total_learning_time = models.IntegerField(default=0, help_text="Temps total en minutes")
    total_courses_enrolled = models.IntegerField(default=0)
    total_courses_completed = models.IntegerField(default=0)
    total_exercises_attempted = models.IntegerField(default=0)
    total_exercises_passed = models.IntegerField(default=0)
    
    # Moyennes
    average_exercise_score = models.FloatField(default=0.0)
    average_course_completion_time = models.IntegerField(default=0)
    average_daily_learning_time = models.IntegerField(default=0)
    
    # Progression
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    
    # Santé d'apprentissage
    learning_consistency = models.FloatField(default=0.0, help_text="Score de cohérence (0-100)")
    motivation_level = models.FloatField(default=50.0, help_text="Niveau de motivation estimé (0-100)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytique utilisateur"
        verbose_name_plural = "Analytiques utilisateur"
    
    def __str__(self):
        return f"Analytics de {self.user.username}"


class CourseAnalytics(models.Model):
    """
    Analyse par cours
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.OneToOneField('content.Course', on_delete=models.CASCADE, related_name='analytics')
    
    # Métriques
    total_enrollments = models.IntegerField(default=0)
    completed_count = models.IntegerField(default=0)
    completion_rate = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    average_time_spent = models.IntegerField(default=0)
    
    # Engagement
    avg_exercises_per_user = models.FloatField(default=0.0)
    dropout_rate = models.FloatField(default=0.0)
    
    # Difficultés
    most_challenging_modules = models.JSONField(default=list)
    user_feedback_score = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Analytique cours"
        verbose_name_plural = "Analytiques cours"
    
    def __str__(self):
        return f"Analytics de {self.course.title}"


class LearningPath(models.Model):
    """
    Parcours d'apprentissage recommandé
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='learning_paths')
    name = models.CharField(max_length=200)
    description = models.TextField()
    courses = models.ManyToManyField('content.Course', related_name='paths')
    
    total_duration_hours = models.FloatField()
    difficulty_progression = models.JSONField(default=list, help_text="Liste des difficultés")
    estimated_completion_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Parcours d'apprentissage"
        verbose_name_plural = "Parcours d'apprentissage"
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"


class DailyMetric(models.Model):
    """
    Métriques quotidiennes pour le suivi
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='daily_metrics')
    date = models.DateField()
    
    learning_time_minutes = models.IntegerField(default=0)
    exercises_attempted = models.IntegerField(default=0)
    exercises_passed = models.IntegerField(default=0)
    videos_watched = models.IntegerField(default=0)
    pages_read = models.IntegerField(default=0)
    
    mood_score = models.FloatField(null=True, blank=True, help_text="Score d'humeur/satisfaction")
    motivation_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Métrique quotidienne"
        verbose_name_plural = "Métriques quotidiennes"
        unique_together = ('user', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"


class PerformanceMetric(models.Model):
    """
    Métriques de performance par domaine/sujet
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='performance_metrics')
    
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    
    total_attempts = models.IntegerField(default=0)
    successful_attempts = models.IntegerField(default=0)
    success_rate = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    
    time_trend = models.JSONField(default=list, help_text="Progression temporelle")
    difficulty_rating = models.FloatField(default=0.0)
    
    last_attempted = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Métrique de performance"
        verbose_name_plural = "Métriques de performance"
        unique_together = ('user', 'subject')
    
    def __str__(self):
        return f"{self.user.username} - {self.subject}"
