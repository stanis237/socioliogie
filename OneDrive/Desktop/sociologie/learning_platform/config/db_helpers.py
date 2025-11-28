# Database Configuration Helpers

def check_database_connection():
    """Vérifier la connexion à la base de données"""
    from django.db import connection
    try:
        connection.ensure_connection()
        return True
    except Exception as e:
        print(f"Erreur de connexion BD: {e}")
        return False

def create_sample_data():
    """Créer des données d'exemple pour le développement"""
    from apps.users.models import CustomUser
    from apps.content.models import Course, Module, Lesson
    from apps.exercises.models import Exercise, Question, Answer
    
    # Créer un utilisateur de test
    if not CustomUser.objects.filter(username='demo').exists():
        user = CustomUser.objects.create_user(
            username='demo',
            email='demo@example.com',
            password='demo123456',
            first_name='Demo',
            last_name='User'
        )
        print(f"✓ Utilisateur demo créé: {user}")
    
    # Créer des cours de test (à implémenter)
    print("✓ Données d'exemple chargées")
