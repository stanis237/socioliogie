from django.db import models
import uuid

class ContentRecommendation(models.Model):
    """
    Recommandations de contenu personnalisées
    """
    RECOMMENDATION_REASONS = [
        ('performance', 'Basé sur la performance'),
        ('learning_style', 'Style d\'apprentissage'),
        ('interests', 'Intérêts'),
        ('proficiency', 'Niveau de compétence'),
        ('emotional_state', 'État émotionnel'),
        ('trend', 'Tendance'),
        ('similar_users', 'Utilisateurs similaires'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='content_recommendations')
    recommended_course = models.ForeignKey('content.Course', on_delete=models.CASCADE, null=True, blank=True)
    recommended_lesson = models.ForeignKey('content.Lesson', on_delete=models.CASCADE, null=True, blank=True)
    
    reason = models.CharField(max_length=50, choices=RECOMMENDATION_REASONS)
    reason_explanation = models.TextField(help_text="Explication transparente pour l'utilisateur")
    
    confidence_score = models.FloatField(help_text="Score de confiance (0-1)")
    priority = models.IntegerField(default=0, help_text="Priorité d'affichage")
    
    is_clicked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    dismissed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Recommandation"
        verbose_name_plural = "Recommandations"
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['confidence_score']),
        ]
    
    def __str__(self):
        course_or_lesson = self.recommended_course or self.recommended_lesson
        return f"{self.user.username} → {course_or_lesson}"


class ExerciseRecommendation(models.Model):
    """
    Recommandations d'exercices adaptatifs
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='exercise_recommendations')
    exercise = models.ForeignKey('exercises.Exercise', on_delete=models.CASCADE)
    
    difficulty_adjusted = models.CharField(max_length=20, choices=[
        ('same', 'Même difficulté'),
        ('easier', 'Plus facile'),
        ('harder', 'Plus difficile'),
    ])
    expected_performance = models.FloatField(help_text="Performance attendue (0-100)")
    reason = models.TextField()
    
    is_attempted = models.BooleanField(default=False)
    is_passed = models.BooleanField(default=False)
    actual_score = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    attempted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Recommandation d'exercice"
        verbose_name_plural = "Recommandations d'exercice"
    
    def __str__(self):
        return f"{self.user.username} → {self.exercise.title}"


class RecommendationLog(models.Model):
    """
    Journal des recommandations pour traçabilité IA
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='recommendation_logs')
    
    # Contexte
    user_profile = models.JSONField(help_text="Profil utilisateur au moment de la recommandation")
    user_performance = models.JSONField(help_text="Métriques de performance")
    user_emotional_state = models.JSONField(null=True, blank=True, help_text="État émotionnel détecté")
    
    # Recommandation
    recommended_items = models.JSONField(help_text="Liste des items recommandés avec scores")
    algorithm_version = models.CharField(max_length=50)
    features_used = models.JSONField(help_text="Features utilisées par l'algorithme")
    
    # Résultats
    user_clicked = models.BooleanField(default=False)
    user_completed = models.BooleanField(default=False)
    user_feedback = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('neutral', 'Neutre'),
        ('negative', 'Négative'),
    ], null=True, blank=True)
    
    feedback_score = models.IntegerField(null=True, blank=True, help_text="Note (1-5)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Journal de recommandation"
        verbose_name_plural = "Journaux de recommandation"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Log {self.user.username} - {self.created_at.date()}"


class AIExplainability(models.Model):
    """
    Explications des décisions IA (Explainable AI)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recommendation = models.OneToOneField(ContentRecommendation, on_delete=models.CASCADE, related_name='explanation')
    
    # Facteurs contribuant
    factors = models.JSONField(help_text="Facteurs influençant la recommandation avec poids")
    primary_factor = models.CharField(max_length=100)
    primary_factor_contribution = models.FloatField(help_text="Contribution du facteur principal (0-1)")
    
    # Explication utilisateur
    user_friendly_explanation = models.TextField(help_text="Explication en langage naturel")
    supporting_data = models.JSONField(help_text="Données justifiant la recommandation")
    
    # Alternatives
    alternative_recommendations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Explainability IA"
        verbose_name_plural = "Explainability IA"
    
    def __str__(self):
        return f"Explication pour {self.recommendation.user.username}"
