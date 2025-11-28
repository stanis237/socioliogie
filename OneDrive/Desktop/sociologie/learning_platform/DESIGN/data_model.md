# Modèle de données (schéma ER) — Plateforme d'apprentissage

Ce document propose un schéma entité‑relation et le mapping vers des modèles Django pour les entités clés : utilisateurs, contenus, recommandations, explicabilité IA, mesures de performance et détection émotionnelle.

## Vue d'ensemble des entités principales
- **User** (utilisateur) — informations de compte et profil (learning_style, préférences).
- **Course / Exercise** (contenu) — métadonnées sur les cours et exercices.
- **ContentRecommendation** — recommandation générée pour un utilisateur, référençant un contenu.
- **AIExplainability** — explication en langage naturel liée à une recommandation.
- **PerformanceMetric** — métriques de performance d'un utilisateur par sujet.
- **EmotionDetection** — détection ponctuelle d'émotion (timestamp, confidence).
- **EmotionalState** — état agrégé par utilisateur (moyennes, tendances).
- **EmotionAdaptation** — adaptation ou action recommandée basée sur l'état émotionnel.

## Relations clés
- `User 1 --- N ContentRecommendation` : un utilisateur peut avoir plusieurs recommandations.
- `ContentRecommendation 1 --- 1 AIExplainability` : chaque recommandation peut avoir une explication IA.
- `User 1 --- N PerformanceMetric` : métriques historiques/agrégées par utilisateur.
- `User 1 --- N EmotionDetection` et `User 1 --- 1 EmotionalState`.

## Contraintes et index
- Index sur `ContentRecommendation(user, recommended_course, created_at)` pour accès rapide.
- TTL / cache: les explications IA peuvent être mises en cache dans Redis; en base, stocker `created_at` et `source`.
- Conserver `supporting_data` en JSON pour les métadonnées hétérogènes.

## Modèles Django recommandés (extraits)

### User (extrait)
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    learning_style = models.CharField(max_length=50, null=True, blank=True)
    preferences = models.JSONField(default=dict, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```

### Course / Exercise (simplifié)
```python
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=30, default='draft')

class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)
    difficulty_level = models.CharField(max_length=50)
```

### ContentRecommendation
```python
class ContentRecommendation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recommendations')
    recommended_course = models.ForeignKey('content.Course', on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    reason_explanation = models.TextField(null=True, blank=True)
    confidence_score = models.FloatField(default=0.0)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user','recommended_course','created_at'])]
```

### AIExplainability
```python
class AIExplainability(models.Model):
    recommendation = models.OneToOneField('recommendations.ContentRecommendation', on_delete=models.CASCADE, related_name='explanation')
    factors = models.JSONField(default=list, blank=True)
    primary_factor = models.CharField(max_length=200, null=True, blank=True)
    primary_factor_contribution = models.FloatField(default=0.0)
    user_friendly_explanation = models.TextField(null=True, blank=True)
    supporting_data = models.JSONField(default=dict, blank=True)
    source = models.CharField(max_length=50, default='ai')
    created_at = models.DateTimeField(auto_now_add=True)
```

### PerformanceMetric
```python
class PerformanceMetric(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    success_rate = models.FloatField(default=0.0)
    average_score = models.FloatField(default=0.0)
    difficulty_rating = models.FloatField(default=0.0)
    total_attempts = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
```

### EmotionDetection & EmotionalState
```python
class EmotionDetection(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    detected_emotion = models.CharField(max_length=50)
    confidence = models.FloatField(default=0.0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class EmotionalState(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='emotional_state')
    average_emotion = models.CharField(max_length=50, null=True, blank=True)
    average_confidence = models.FloatField(default=0.0)
    mood_trend = models.JSONField(default=dict, blank=True)
    stress_level = models.FloatField(default=0.0)
    engagement_level = models.FloatField(default=0.0)
    fatigue_level = models.FloatField(default=0.0)
    last_calculated = models.DateTimeField(auto_now=True)
```

### EmotionAdaptation
```python
class EmotionAdaptation(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    emotion_detection = models.ForeignKey('emotions.EmotionDetection', null=True, on_delete=models.SET_NULL)
    adaptation_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    message_to_user = models.TextField(null=True, blank=True)
    new_difficulty = models.CharField(max_length=50, null=True, blank=True)
    new_content_type = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## Notes d'implémentation
- Préférer `JSONField` pour données hétérogènes (factors, supporting_data).
- Ne pas stocker d'informations d'identification personnelles dans les prompts envoyés à OpenAI.
- Utiliser `OneToOneField` pour `AIExplainability` afin de garantir qu'une recommandation n'ait qu'une seule explication canonique.
- Pour la migration: créer d'abord les modèles en lecture (sans contraintes strictes), migrer les données, puis appliquer contraintes additionnelles.

## Propositions de modifications aux fichiers existants
- Vérifier `apps/recommendations/models.py` et s'assurer que `AIExplainability` existe et qu'il a les champs indiqués ci‑dessus.
- Vérifier `apps/content/models.py` pour la présence des champs `status`, `level`, `duration_minutes`.
- Ajouter index sur `ContentRecommendation` si absent.

---
Je peux maintenant :
- générer automatiquement les migrations / patchs pour `apps/*/models.py` (à votre validation), ou
- seulement produire les fichiers de design et laisser l'implémentation pour une étape suivante.

Que préférez-vous ? (implémenter maintenant / seulement doc)
