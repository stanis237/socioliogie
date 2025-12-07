from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    level = models.CharField(max_length=50, default='beginner', choices=[
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    ])
    school_level = models.CharField(max_length=50, default='secondary', choices=[
        ('primary', 'Primaire'),
        ('secondary', 'Secondaire'),
        ('university', 'Université'),
        ('professional', 'Formation professionnelle'),
    ], verbose_name='Niveau scolaire')
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile de {self.user.username}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Historique(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historique')
    content_type = models.CharField(max_length=50, choices=[
        ('course', 'Cours'),
        ('video', 'Vidéo'),
        ('document', 'Document'),
        ('quiz', 'Quiz'),
        ('exercise', 'Exercice'),
    ])
    content_id = models.IntegerField()
    progress = models.IntegerField(default=0)  # Pourcentage de complétion
    completed = models.BooleanField(default=False)
    last_accessed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_accessed']
        unique_together = ['user', 'content_type', 'content_id']

    def __str__(self):
        return f"{self.user.username} - {self.content_type} #{self.content_id}"
