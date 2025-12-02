from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    ]
    
    SUBJECT_CHOICES = [
        ('sociology', 'Sociologie'),
        ('mathematics', 'Mathématiques'),
        ('science', 'Sciences'),
        ('history', 'Histoire'),
        ('literature', 'Littérature'),
        ('philosophy', 'Philosophie'),
        ('psychology', 'Psychologie'),
        ('economics', 'Économie'),
        ('languages', 'Langues'),
        ('arts', 'Arts'),
        ('geography', 'Géographie'),
        ('computer_science', 'Informatique'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='intermediate')
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='sociology', verbose_name='Matière')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    duration = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: 10:30, 1h 15min")

    def __str__(self):
        return self.title

class Document(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    questions = models.JSONField()

    def __str__(self):
        return self.title

class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=50, choices=[('easy', 'Facile'), ('medium', 'Moyen'), ('hard', 'Difficile')])
    content = models.TextField()

    def __str__(self):
        return self.title
