from django.db import models
import uuid

class Notification(models.Model):
    """
    Modèle pour les notifications
    """
    NOTIFICATION_TYPES = [
        ('reminder', 'Rappel'),
        ('achievement', 'Accomplissement'),
        ('recommendation', 'Recommandation'),
        ('message', 'Message'),
        ('alert', 'Alerte'),
        ('encouragement', 'Encouragement'),
        ('milestone', 'Jalon'),
        ('course_update', 'Mise à jour cours'),
    ]
    
    CHANNELS = [
        ('in_app', 'Dans l\'application'),
        ('email', 'Email'),
        ('push', 'Notification Push'),
        ('sms', 'SMS'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='notifications')
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    
    # Ciblage
    channel = models.CharField(max_length=50, choices=CHANNELS, default='in_app')
    priority = models.IntegerField(default=0, help_text="Priorité (0-10)")
    
    # Adaptation
    personalized = models.BooleanField(default=True, help_text="Adaptée au profil")
    emotional_state_aware = models.BooleanField(default=False, help_text="Adaptée à l'état émotionnel")
    
    # Métadonnées
    related_content = models.CharField(max_length=500, blank=True, help_text="JSON de contenu lié")
    action_url = models.CharField(max_length=500, blank=True)
    
    # Suivi
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    clicked = models.BooleanField(default=False)
    
    read_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['is_read']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationPreference(models.Model):
    """
    Préférences utilisateur pour les notifications
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Canaux
    enable_email = models.BooleanField(default=True)
    enable_push = models.BooleanField(default=True)
    enable_in_app = models.BooleanField(default=True)
    enable_sms = models.BooleanField(default=False)
    
    # Types
    enable_reminders = models.BooleanField(default=True)
    enable_achievements = models.BooleanField(default=True)
    enable_recommendations = models.BooleanField(default=True)
    enable_messages = models.BooleanField(default=True)
    enable_alerts = models.BooleanField(default=True)
    enable_encouragement = models.BooleanField(default=True)
    
    # Timing
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_hours_start = models.TimeField(null=True, blank=True, help_text="HH:MM")
    quiet_hours_end = models.TimeField(null=True, blank=True, help_text="HH:MM")
    
    # Fréquence
    email_frequency = models.CharField(max_length=20, default='daily', choices=[
        ('instant', 'Immédiat'),
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('never', 'Jamais'),
    ])
    
    # Confidentialité
    allow_personalization = models.BooleanField(default=True)
    allow_emotional_adaptation = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Préférence de notification"
        verbose_name_plural = "Préférences de notification"
    
    def __str__(self):
        return f"Préférences de {self.user.username}"


class EmailTemplate(models.Model):
    """
    Templates pour les emails
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True, help_text="Code unique pour le template")
    description = models.TextField()
    
    subject = models.CharField(max_length=200)
    html_content = models.TextField()
    text_content = models.TextField()
    
    # Variables disponibles
    available_variables = models.JSONField(default=list)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Template Email"
        verbose_name_plural = "Templates Email"
    
    def __str__(self):
        return self.name


class NotificationSchedule(models.Model):
    """
    Programmation des notifications récurrentes
    """
    FREQUENCIES = [
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('custom', 'Personnalisé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='notification_schedules')
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=Notification.NOTIFICATION_TYPES)
    
    frequency = models.CharField(max_length=50, choices=FREQUENCIES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    time = models.TimeField(help_text="Heure d'envoi (HH:MM)")
    
    # Jours
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Programmation de notification"
        verbose_name_plural = "Programmations de notification"
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class NotificationLog(models.Model):
    """
    Journal des notifications envoyées
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    
    channel = models.CharField(max_length=50, choices=Notification.CHANNELS)
    recipient = models.CharField(max_length=255, help_text="Email ou téléphone")
    status = models.CharField(max_length=50, choices=[
        ('sent', 'Envoyé'),
        ('failed', 'Échoué'),
        ('bounced', 'Rejeté'),
        ('unsubscribed', 'Désinscrit'),
    ])
    
    message_id = models.CharField(max_length=255, blank=True)
    error_message = models.TextField(blank=True)
    
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Journal de notification"
        verbose_name_plural = "Journaux de notification"
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.notification.user.username} - {self.status}"
