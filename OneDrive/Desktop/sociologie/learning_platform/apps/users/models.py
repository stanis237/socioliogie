from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
import uuid

class CustomUser(AbstractUser):
    """
    Modèle utilisateur personnalisé avec informations supplémentaires
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    LEARNING_STYLES = [
        ('visual', 'Visuel'),
        ('auditory', 'Auditif'),
        ('kinesthetic', 'Kinesthésique'),
        ('reading', 'Lecture/Écriture'),
    ]

    PROFICIENCY_LEVELS = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLES, default='visual')
    proficiency_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='beginner')
    interests = models.JSONField(default=list, help_text="List of user interests")
    goals = models.JSONField(default=list, help_text="Learning goals")
    daily_goal_minutes = models.IntegerField(default=30)
    timezone = models.CharField(max_length=50, default='Europe/Paris')
    notification_enabled = models.BooleanField(default=True)
    emotion_tracking_enabled = models.BooleanField(default=False)
    webcam_consent = models.BooleanField(default=False, help_text="Consent for emotion recognition via webcam")
    privacy_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_active_learner = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class UserProfile(models.Model):
    """
    Extended user profile for detailed tracking
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='detailed_profile')
    total_learning_minutes = models.IntegerField(default=0)
    exercises_completed = models.IntegerField(default=0)
    average_score = models.FloatField(default=0.0)
    streaks_days = models.IntegerField(default=0)
    last_streak_date = models.DateField(null=True, blank=True)
    badges = models.JSONField(default=list)
    preference_notifications = models.BooleanField(default=True)
    preference_email_digests = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
    
    def __str__(self):
        return f"Profile de {self.user.get_full_name()}"


class UserActivityLog(models.Model):
    """
    Track all user activities for analytics
    """
    ACTIVITY_TYPES = [
        ('login', 'Connexion'),
        ('logout', 'Déconnexion'),
        ('view_content', 'Consultation contenu'),
        ('complete_exercise', 'Exercice complété'),
        ('video_watched', 'Vidéo regardée'),
        ('quiz_completed', 'Quiz complété'),
        ('forum_post', 'Message forum'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Journal d'activité"
        verbose_name_plural = "Journaux d'activité"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.timestamp}"


class UserSettings(models.Model):
    """
    User-specific settings and preferences
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='settings')
    theme = models.CharField(max_length=20, default='light', choices=[('light', 'Light'), ('dark', 'Dark')])
    language = models.CharField(max_length=10, default='fr', choices=[('fr', 'Français'), ('en', 'English')])
    font_size = models.CharField(max_length=10, default='medium')
    auto_play_videos = models.BooleanField(default=True)
    subtitles_enabled = models.BooleanField(default=False)
    notifications_email = models.BooleanField(default=True)
    notifications_push = models.BooleanField(default=True)
    notifications_sms = models.BooleanField(default=False)
    allow_analytics = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Paramètres utilisateur"
        verbose_name_plural = "Paramètres utilisateurs"
    
    def __str__(self):
        return f"Paramètres de {self.user.username}"
