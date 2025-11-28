from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class EmotionDetection(models.Model):
    """
    Détection des émotions via webcam
    """
    EMOTIONS = [
        ('happy', 'Heureux'),
        ('sad', 'Triste'),
        ('angry', 'En colère'),
        ('neutral', 'Neutre'),
        ('surprised', 'Surpris'),
        ('fearful', 'Apeuré'),
        ('disgusted', 'Dégoûté'),
        ('tired', 'Fatigué'),
        ('focused', 'Concentré'),
        ('confused', 'Confus'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='emotion_detections')
    
    # Émotion détectée
    detected_emotion = models.CharField(max_length=50, choices=EMOTIONS, help_text="Émotion principale détectée")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    
    # Détails
    emotion_scores = models.JSONField(help_text="Scores pour chaque émotion")
    facial_features = models.JSONField(help_text="Données des traits faciaux détectées")
    
    # Contexte
    activity_context = models.CharField(max_length=200, blank=True, help_text="Activité pendant la détection")
    exercise_id = models.ForeignKey('exercises.Exercise', on_delete=models.SET_NULL, null=True, blank=True)
    lesson_id = models.ForeignKey('content.Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Adaptation
    recommended_action = models.CharField(max_length=200, blank=True, help_text="Action recommandée par l'IA")
    
    # Données anonymisées pour conformité RGPD
    anonymized_image_hash = models.CharField(max_length=255, blank=True)
    is_anonymized = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Détection d'émotion"
        verbose_name_plural = "Détections d'émotion"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['detected_emotion']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.detected_emotion} ({self.confidence:.2f})"


class EmotionalState(models.Model):
    """
    État émotionnel agrégé pour un utilisateur
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='emotional_state')
    
    # États moyens
    average_emotion = models.CharField(max_length=50, choices=EmotionDetection.EMOTIONS)
    average_confidence = models.FloatField(default=0.0)
    
    # Tendances
    mood_trend = models.CharField(max_length=20, choices=[
        ('improving', 'Amélioration'),
        ('declining', 'Détérioration'),
        ('stable', 'Stable'),
    ])
    
    # Métriques
    stress_level = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    engagement_level = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    fatigue_level = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    
    # Recommandations
    needs_break = models.BooleanField(default=False)
    recommended_break_duration = models.IntegerField(null=True, blank=True, help_text="Durée recommandée en minutes")
    needs_support = models.BooleanField(default=False)
    support_type = models.CharField(max_length=100, blank=True)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "État émotionnel"
        verbose_name_plural = "États émotionnels"
    
    def __str__(self):
        return f"État émotionnel de {self.user.username}"


class EmotionAdaptation(models.Model):
    """
    Adaptations du cours basées sur l'état émotionnel
    """
    ADAPTATION_TYPES = [
        ('break', 'Pause recommandée'),
        ('difficulty_adjust', 'Ajustement de difficulté'),
        ('change_content_type', 'Changement de type de contenu'),
        ('motivation_message', 'Message de motivation'),
        ('slower_pace', 'Rythme plus lent'),
        ('faster_pace', 'Rythme plus rapide'),
        ('support_resources', 'Ressources de support'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='emotion_adaptations')
    emotion_detection = models.ForeignKey(EmotionDetection, on_delete=models.CASCADE)
    
    adaptation_type = models.CharField(max_length=50, choices=ADAPTATION_TYPES)
    description = models.TextField()
    message_to_user = models.TextField()
    
    # Configuration
    new_difficulty = models.CharField(max_length=20, blank=True, choices=[
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
    ])
    new_content_type = models.CharField(max_length=50, blank=True)
    recommended_resource = models.CharField(max_length=500, blank=True)
    
    # Réponse utilisateur
    user_accepted = models.BooleanField(null=True, blank=True)
    effectiveness = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Adaptation émotionnelle"
        verbose_name_plural = "Adaptations émotionnelles"
    
    def __str__(self):
        return f"{self.user.username} - {self.adaptation_type}"


class EmotionFeedback(models.Model):
    """
    Feedback utilisateur sur les détections émotionnelles
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='emotion_feedbacks')
    emotion_detection = models.ForeignKey(EmotionDetection, on_delete=models.CASCADE)
    
    # Feedback
    is_accurate = models.BooleanField(help_text="La détection était-elle correcte?")
    actual_emotion = models.CharField(max_length=50, choices=EmotionDetection.EMOTIONS, blank=True)
    comments = models.TextField(blank=True)
    
    # Note
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Feedback d'émotion"
        verbose_name_plural = "Feedbacks d'émotion"
    
    def __str__(self):
        return f"{self.user.username} - {self.emotion_detection}"


class EmotionalTrend(models.Model):
    """
    Analyse des tendances émotionnelles
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='emotional_trends')
    
    # Période
    date = models.DateField()
    
    # Données
    dominant_emotion = models.CharField(max_length=50, choices=EmotionDetection.EMOTIONS)
    emotion_distribution = models.JSONField(help_text="Distribution des émotions par jour")
    
    # Corrélations
    correlation_with_performance = models.FloatField(null=True, blank=True)
    correlation_with_activities = models.JSONField(default=dict)
    
    # Recommandations
    insights = models.TextField(blank=True)
    recommendations = models.JSONField(default=list)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tendance émotionnelle"
        verbose_name_plural = "Tendances émotionnelles"
        unique_together = ('user', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"
