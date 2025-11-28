#!/usr/bin/env python
"""
Commandes de gestion personnalisées pour la plateforme
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.analytics.models import UserAnalytics, DailyMetric
from apps.recommendations.models import ContentRecommendation
from apps.users.models import CustomUser
from apps.content.models import Course, EnrolledCourse
from apps.exercises.models import ExerciseSubmission
from ai_module.services import RecommendationService, EmotionService
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Commandes de gestion de la plateforme d'apprentissage"

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action à exécuter')
        parser.add_argument('--user-id', type=str, help='ID utilisateur')

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'generate-recommendations':
            self.generate_recommendations(options.get('user_id'))
        elif action == 'analyze-emotions':
            self.analyze_emotions(options.get('user_id'))
        elif action == 'update-statistics':
            self.update_statistics(options.get('user_id'))
        elif action == 'cleanup-old-data':
            self.cleanup_old_data()
        else:
            self.stdout.write(f"Action inconnue: {action}")

    def generate_recommendations(self, user_id=None):
        """Générer les recommandations pour les utilisateurs"""
        self.stdout.write("Génération des recommandations...")
        
        if user_id:
            users = CustomUser.objects.filter(id=user_id)
        else:
            users = CustomUser.objects.all()
        
        for user in users:
            try:
                # Supprimer les anciennes recommandations non visitées
                ContentRecommendation.objects.filter(
                    user=user,
                    is_clicked=False,
                    is_completed=False
                ).delete()
                
                # Générer les nouvelles
                recs = RecommendationService.generate_recommendations(user, limit=5)
                RecommendationService.save_recommendations(user, recs)
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ {len(recs)} recommandations générées pour {user.username}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Erreur pour {user.username}: {e}")
                )

    def analyze_emotions(self, user_id=None):
        """Analyser les états émotionnels"""
        self.stdout.write("Analyse des états émotionnels...")
        
        if user_id:
            users = CustomUser.objects.filter(id=user_id)
        else:
            users = CustomUser.objects.filter(emotion_tracking_enabled=True)
        
        for user in users:
            try:
                analysis = EmotionService.analyze_emotion_state(user)
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Analyse complétée pour {user.username}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Erreur pour {user.username}: {e}")
                )

    def update_statistics(self, user_id=None):
        """Mettre à jour les statistiques d'apprentissage"""
        self.stdout.write("Mise à jour des statistiques...")
        
        if user_id:
            users = CustomUser.objects.filter(id=user_id)
        else:
            users = CustomUser.objects.all()
        
        for user in users:
            try:
                analytics, created = UserAnalytics.objects.get_or_create(user=user)
                
                # Calculer les nouvelles métriques
                enrollments = EnrolledCourse.objects.filter(user=user)
                submissions = ExerciseSubmission.objects.filter(user=user, status='submitted')
                
                analytics.total_courses_enrolled = enrollments.count()
                analytics.total_courses_completed = enrollments.filter(completed_at__isnull=False).count()
                analytics.total_exercises_attempted = submissions.count()
                analytics.total_exercises_passed = submissions.filter(percentage__gte=70).count()
                
                if submissions.exists():
                    scores = [s.percentage for s in submissions if s.percentage]
                    analytics.average_exercise_score = sum(scores) / len(scores) if scores else 0
                
                analytics.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Statistiques mises à jour pour {user.username}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Erreur pour {user.username}: {e}")
                )

    def cleanup_old_data(self):
        """Nettoyer les données anciennes"""
        self.stdout.write("Nettoyage des données anciennes...")
        
        from datetime import timedelta
        threshold = timezone.now() - timedelta(days=90)
        
        # Supprimer les recommandations anciendes et rejetées
        deleted, _ = ContentRecommendation.objects.filter(
            created_at__lt=threshold,
            dismissed=True
        ).delete()
        self.stdout.write(f"✓ {deleted} recommandations supprimées")
