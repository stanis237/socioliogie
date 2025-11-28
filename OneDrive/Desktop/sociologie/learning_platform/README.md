# Plateforme d'Apprentissage Personnalisé avec IA Innovante

Une plateforme web complète d'apprentissage adaptatif avec intelligence artificielle, analyse émotionnelle et recommandations personnalisées.

## Caractéristiques principales

### 1. **Gestion des profils utilisateurs**
- Création/édition/suppression de comptes
- Profils détaillés avec styles d'apprentissage (visuel, auditif, kinesthésique, lecture)
- Historique des activités et résultats
- Gestion des préférences et consentements RGPD

### 2. **Contenu et exercices personnalisés**
- Bibliothèque complète de cours, vidéos et documents
- Génération dynamique de quizz adaptatifs
- Exercices de différents types (QCM, essais, codage, appariement, etc.)
- Système adaptatif ajustant la difficulté selon la progression

### 3. **Recommandations intelligentes avec IA explicable**
- Algorithme collaboratif et content-based
- Explications transparentes des recommandations
- Adaptation selon le profil, résultats et émotions
- Traçabilité complète des décisions IA

### 4. **Analyse émotionnelle adaptative**
- Reconnaissance faciale via webcam (avec consentement)
- Détection des émotions (heureux, stressed, fatigué, concentré, etc.)
- Adaptation automatique du rythme et du contenu
- Stockage sécurisé et anonymisé des données

### 5. **Suivi et analytique**
- Dashboard personnalisé avec synthèse graphique
- Métriques de performance par domaine
- Tendances d'apprentissage et d'engagement
- Parcours d'apprentissage recommandés

### 6. **Notifications intelligentes**
- Rappels auto-adaptés selon l'engagement
- Encouragements personnalisés
- Programmation intelligente des notifications
- Respect des préférences utilisateur

### 7. **Sécurité et RGPD**
- Authentification sécurisée avec JWT
- Chiffrement des données sensibles
- Gestion du consentement pour tous les services
- Anonymisation des données d'analyse émotionnelle
- Audit logs complets

## Architecture technique

### Stack technologique
- **Frontend**: React.js (responsive, PWA ready)
- **Backend**: Django 4.2 + Django REST Framework
- **BD**: MySQL avec ORM Django
- **IA/ML**: Python (scikit-learn, TensorFlow, OpenCV)
- **Temps réel**: Redis + Celery
- **Cloud**: AWS/Azure/GCP compatible
- **API**: RESTful avec documentation Swagger

### Structure des applications Django

```
learning_platform/
├── config/               # Configuration Django
├── apps/
│   ├── users/           # Gestion des utilisateurs
│   ├── content/         # Cours, modules, leçons
│   ├── exercises/       # Exercices, quizz, submissions
│   ├── analytics/       # Analytique et suivi
│   ├── recommendations/ # Moteur de recommandations
│   ├── emotions/        # Analyse émotionnelle
│   └── notifications/   # Système de notifications
├── ai_module/           # Module IA
├── static/              # Fichiers statiques
├── media/               # Uploads utilisateurs
└── logs/                # Logs système
```

## Installation et démarrage

### Prérequis
- Python 3.9+
- MySQL 8.0+
- Redis 6.0+
- Node.js 16+ (pour React)

### Étapes d'installation

1. **Cloner le projet**
```bash
git clone <repo_url>
cd learning_platform
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer l'environnement**
```bash
cp .env.example .env
# Éditer .env avec vos paramètres
```

5. **Initialiser la base de données**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Lancer le serveur**
```bash
python manage.py runserver
# L'API sera disponible sur http://localhost:8000/
# Admin sur http://localhost:8000/admin/
```

## API Endpoints

### Authentification et Utilisateurs
- `POST /api/users/register/` - Inscription
- `GET /api/users/me/` - Profil actuel
- `PUT /api/users/update_me/` - Mettre à jour le profil
- `GET /api/users/settings/` - Paramètres utilisateur
- `POST /api/users/enable_emotion_tracking/` - Activer suivi émotionnel

### Contenu
- `GET /api/content/courses/` - Lister les cours
- `POST /api/content/courses/{id}/enroll/` - S'inscrire
- `GET /api/content/courses/my_courses/` - Mes cours
- `GET /api/content/lessons/` - Leçons

### Exercices
- `GET /api/exercises/exercises/` - Lister les exercices
- `POST /api/exercises/submissions/start_exercise/` - Commencer un exercice
- `POST /api/exercises/submissions/{id}/submit_exercise/` - Soumettre

### Recommandations
- `GET /api/recommendations/content/get_recommendations/` - Recommandations
- `GET /api/recommendations/content/{id}/explanation/` - Explication IA

### Émotions
- `POST /api/emotions/detections/upload_emotion_data/` - Upload émotion
- `GET /api/emotions/state/current_state/` - État émotionnel actuel

### Analytique
- `GET /api/analytics/user/my_analytics/` - Mes statistiques
- `GET /api/analytics/daily-metrics/` - Métriques quotidiennes

### Notifications
- `GET /api/notifications/` - Mes notifications
- `POST /api/notifications/{id}/mark_as_read/` - Marquer comme lu
- `GET /api/notifications/unread_count/` - Nombre non lus

## Fonctionnalités IA

### Recommandation Engine
```python
from ai_module.services import RecommendationService

# Générer les recommandations
recommendations = RecommendationService.generate_recommendations(user, limit=5)

# Sauvegarder
RecommendationService.save_recommendations(user, recommendations)
```

### Analyse Émotionnelle
```python
from ai_module.services import EmotionService

# Analyser l'état émotionnel
analysis = EmotionService.analyze_emotion_state(user)

# Créer une adaptation
adaptation = EmotionService.create_adaptation(user, emotion_detection, emotional_state)
```

### Adaptation de difficulté
```python
from ai_module.services import DifficultyAdaptationService

# Obtenir la difficulté adaptée
difficulty = DifficultyAdaptationService.get_adaptive_difficulty(user, exercise)
```

## Modèles de données principaux

### CustomUser
Utilisateur avec profil détaillé, style d'apprentissage, objectifs

### Course, Module, Lesson
Structure hiérarchique du contenu pédagogique

### Exercise, Question, Answer
Système d'évaluation avec support multi-types

### ContentRecommendation, AIExplainability
Recommandations avec explications transparentes

### EmotionDetection, EmotionalState, EmotionAdaptation
Système d'analyse émotionnelle et adaptation

### UserAnalytics, DailyMetric, PerformanceMetric
Analytique complète avec suivi quotidien

## Authentification API

Utilisez l'authentification JWT. Exemple:

```javascript
// Login
POST /api/auth/login/
{
  "username": "user@example.com",
  "password": "password"
}

// Response
{
  "access": "token...",
  "refresh": "token..."
}

// Utiliser dans les requêtes
Authorization: Bearer <token>
```

## Configuration RGPD

### Consentements
- Consentement d'utilisation des données
- Consentement webcam pour analyse émotionnelle
- Consentement email/SMS

### Anonymisation
- Données émotionnelles anonymisées automatiquement
- Hashage des images faciales
- Suppression des données après délai configurable

### Droits
- Exportation des données personnelles
- Suppression du compte et données associées
- Accès à tous les logs d'activité

## Déploiement

### Docker
```bash
docker-compose up
```

### Cloud (AWS/Azure/GCP)
Voir documentation de déploiement dans `docs/deployment/`

## Tests

```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov

# Tests spécifiques
pytest apps/users/tests/
```

## Documentation

- API Swagger: http://localhost:8000/swagger/
- Architecture: `docs/architecture.md`
- Guides d'utilisation: `docs/guides/`

## Support et contribution

Pour toute question ou contribution, consultez notre guide de contribution.

## Licence

MIT License

## Auteur

Développé en 2024
