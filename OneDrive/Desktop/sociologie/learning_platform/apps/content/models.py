from django.db import models
from django.utils import timezone
import uuid

class Course(models.Model):
    """
    Modèle pour les cours
    """
    DIFFICULTY_LEVELS = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
        ('expert', 'Expert'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('archived', 'Archivé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    summary = models.CharField(max_length=500)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    category = models.CharField(max_length=100)
    tags = models.JSONField(default=list)
    instructor = models.CharField(max_length=200)
    cover_image = models.ImageField(upload_to='courses/')
    video_intro = models.URLField(blank=True)
    duration_hours = models.FloatField(help_text="Durée estimée en heures")
    prerequisites = models.JSONField(default=list, help_text="IDs des cours préalables")
    learning_outcomes = models.JSONField(default=list)
    
    students_enrolled = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    reviews_count = models.IntegerField(default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category']),
            models.Index(fields=['difficulty_level']),
        ]
    
    def __str__(self):
        return self.title
    
    def publish(self):
        self.status = 'published'
        self.published_at = timezone.now()
        self.save()


class Module(models.Model):
    """
    Modèle pour les modules (chapitres) d'un cours
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField()
    duration_minutes = models.IntegerField()
    is_locked = models.BooleanField(default=False)
    unlock_condition = models.CharField(max_length=200, blank=True, help_text="Condition pour débloquer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        ordering = ['course', 'order']
        unique_together = ('course', 'order')
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Lesson(models.Model):
    """
    Modèle pour les leçons (contenu détaillé)
    """
    CONTENT_TYPES = [
        ('text', 'Texte'),
        ('video', 'Vidéo'),
        ('article', 'Article'),
        ('interactive', 'Interactif'),
        ('document', 'Document'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    description = models.TextField()
    order = models.IntegerField()
    duration_minutes = models.IntegerField()
    
    # Contenu
    text_content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    video_duration = models.IntegerField(blank=True, null=True, help_text="Durée vidéo en secondes")
    document_file = models.FileField(upload_to='lessons/documents/', blank=True)
    external_url = models.URLField(blank=True)
    
    # Métadonnées
    learning_objectives = models.JSONField(default=list)
    keywords = models.JSONField(default=list)
    difficulty_level = models.CharField(max_length=20, choices=[('easy', 'Facile'), ('medium', 'Moyen'), ('hard', 'Difficile')])
    
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Leçon"
        verbose_name_plural = "Leçons"
        ordering = ['module', 'order']
        unique_together = ('module', 'order')
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Resource(models.Model):
    """
    Ressources supplémentaires (documents, liens, etc.)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=50, choices=[
        ('document', 'Document'),
        ('link', 'Lien'),
        ('tool', 'Outil'),
        ('reference', 'Référence'),
    ])
    file = models.FileField(upload_to='resources/', blank=True)
    url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class EnrolledCourse(models.Model):
    """
    Suivi de l'inscription des utilisateurs aux cours
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='enrolled_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.FloatField(default=0.0)
    lessons_completed = models.IntegerField(default=0)
    current_module = models.ForeignKey(Module, on_delete=models.SET_NULL, null=True, blank=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Cours inscrit"
        verbose_name_plural = "Cours inscrits"
        unique_together = ('user', 'course')
        ordering = ['-enrolled_at']
        indexes = [
            models.Index(fields=['user', '-enrolled_at']),
            models.Index(fields=['course']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
