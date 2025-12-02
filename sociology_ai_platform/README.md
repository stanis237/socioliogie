# Plateforme d'Apprentissage Sociologie IA

Une plateforme d'apprentissage en ligne pour la sociologie avec des fonctionnalités d'intelligence artificielle adaptative.

## Fonctionnalités

### 🎓 Gestion des Cours
- Liste des cours disponibles
- Détails des cours avec vidéos, documents, quiz et exercices
- Suivi de progression

### 👤 Gestion des Comptes
- Inscription et connexion utilisateurs
- Profils utilisateurs avec avatar, biographie et niveau
- Système de points et de progression
- Historique d'apprentissage

### 📊 Analytics et Recommandations
- Tableau de bord personnalisé avec statistiques
- Recommandations de cours basées sur l'IA
- Enregistrement des données émotionnelles
- Suivi de progression

### 💬 Forum Social
- Création et discussion de posts
- Système de commentaires
- Notifications

## Installation

1. **Cloner le projet** (ou naviguer vers le répertoire)

2. **Installer les dépendances**:
```bash
pip install -r requirements.txt
```

3. **Appliquer les migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Créer un superutilisateur** (optionnel):
```bash
python manage.py createsuperuser
```

5. **Lancer le serveur de développement**:
```bash
python manage.py runserver
```

6. **Accéder à l'application**:
- Site web: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Structure du Projet

```
sociology_ai_platform/
├── accounts/          # Gestion des utilisateurs et profils
├── analytics/         # Analytics, recommandations et données émotionnelles
├── content/           # Cours, vidéos, documents, quiz, exercices
├── social/            # Forum, posts, commentaires, notifications
├── sociology_ai/      # Configuration du projet Django
├── templates/         # Templates HTML avec Bootstrap
├── static/            # Fichiers statiques (CSS, JS, images)
└── media/             # Fichiers médias uploadés (avatars, documents)
```

## Technologies Utilisées

- **Django 5.2+**: Framework web Python
- **Bootstrap 5.3**: Framework CSS pour le design responsive
- **Bootstrap Icons**: Icônes
- **SQLite**: Base de données (par défaut)

## Applications Django

### accounts
- `UserProfile`: Profil utilisateur étendu
- `Historique`: Historique d'apprentissage

### content
- `Course`: Cours
- `Video`: Vidéos de cours
- `Document`: Documents PDF, etc.
- `Quiz`: Quiz avec questions JSON
- `Exercise`: Exercices pratiques

### analytics
- `Recommendation`: Recommandations de cours
- `EmotionData`: Données émotionnelles de l'utilisateur

### social
- `Post`: Posts du forum
- `Comment`: Commentaires sur les posts
- `Notification`: Notifications utilisateur

## Utilisation

1. **Créer un compte** via la page d'inscription
2. **Explorer les cours** disponibles
3. **Consulter le tableau de bord** pour voir votre progression
4. **Participer au forum** pour échanger avec d'autres apprenants
5. **Enregistrer vos émotions** pour des recommandations personnalisées

## Développement

Pour ajouter du contenu, utilisez l'interface d'administration Django:
- Accédez à `/admin/`
- Connectez-vous avec un compte superutilisateur
- Ajoutez des cours, vidéos, documents, etc.

## Notes

- Le projet utilise SQLite par défaut (développement)
- Pour la production, configurez une base de données PostgreSQL ou MySQL
- Les fichiers médias sont stockés dans le répertoire `media/`
- Les fichiers statiques sont collectés dans `staticfiles/` pour la production

## Auteur

Plateforme d'Apprentissage Sociologie IA

## Licence

Ce projet est un projet éducatif.

