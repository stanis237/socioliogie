#!/usr/bin/env python
"""
Script pour migrer les données de SQLite vers PostgreSQL
Exécutez ce script après avoir configuré PostgreSQL
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au chemin Python
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sociology_ai.settings')
django.setup()

from django.core.management import call_command
from django.db import transaction
from accounts.models import UserProfile, Historique
from content.models import Course, Video, Document, Quiz, Exercise
from analytics.models import EmotionData, Recommendation
from social.models import Post, Comment, Notification

def migrate_data():
    """
    Migre les données de SQLite vers PostgreSQL
    """
    print("Début de la migration des données...")

    try:
        # Créer les migrations si nécessaire
        print("Création des migrations...")
        call_command('makemigrations')

        # Appliquer les migrations
        print("Application des migrations...")
        call_command('migrate')

        print("Migration terminée avec succès !")
        print("\nInstructions pour la production :")
        print("1. Installez PostgreSQL sur votre serveur")
        print("2. Créez une base de données : CREATE DATABASE sociology_ai_db;")
        print("3. Créez un utilisateur : CREATE USER postgres WITH PASSWORD 'votre_mot_de_passe';")
        print("4. Accordez les permissions : GRANT ALL PRIVILEGES ON DATABASE sociology_ai_db TO postgres;")
        print("5. Configurez les variables d'environnement :")
        print("   - DB_NAME=sociology_ai_db")
        print("   - DB_USER=postgres")
        print("   - DB_PASSWORD=votre_mot_de_passe")
        print("   - DB_HOST=localhost")
        print("   - DB_PORT=5432")

    except Exception as e:
        print(f"Erreur lors de la migration : {e}")
        print("Assurez-vous que PostgreSQL est installé et configuré.")

if __name__ == '__main__':
    migrate_data()
