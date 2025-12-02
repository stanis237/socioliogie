from django.db import models
from django.contrib.auth.models import User
from content.models import Course

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(default=0.0)  # Score de recommandation (0-1)
    reason = models.TextField(blank=True, null=True)  # Raison de la recommandation
    created_at = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-score', '-created_at']
        unique_together = ['user', 'course']

    def __str__(self):
        return f"Recommandation pour {self.user.username}: {self.course.title}"

class EmotionData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_data')
    emotion_type = models.CharField(max_length=50, choices=[
        ('happy', 'Heureux'),
        ('sad', 'Triste'),
        ('neutral', 'Neutre'),
        ('focused', 'Concentré'),
        ('confused', 'Confus'),
        ('excited', 'Excité'),
    ])
    intensity = models.FloatField(default=0.5)  # Intensité de l'émotion (0-1)
    context = models.CharField(max_length=200, blank=True, null=True)  # Contexte (ex: "pendant un quiz")
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.user.username} - {self.emotion_type} ({self.intensity})"
