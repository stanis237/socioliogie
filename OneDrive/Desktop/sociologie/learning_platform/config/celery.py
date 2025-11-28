"""
Celery Configuration for async tasks
"""
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('learning_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic Tasks
app.conf.beat_schedule = {
    # Générer les recommandations quotidiennement
    'generate-recommendations': {
        'task': 'apps.recommendations.tasks.generate_daily_recommendations',
        'schedule': crontab(hour=2, minute=0),  # 2h du matin
    },
    # Analyser les tendances émotionnelles
    'analyze-emotions': {
        'task': 'apps.emotions.tasks.analyze_emotion_trends',
        'schedule': crontab(hour=3, minute=0),  # 3h du matin
    },
    # Envoyer les notifications programmées
    'send-scheduled-notifications': {
        'task': 'apps.notifications.tasks.send_scheduled_notifications',
        'schedule': crontab(minute='*/15'),  # Toutes les 15 minutes
    },
    # Mettre à jour les statistiques
    'update-statistics': {
        'task': 'apps.analytics.tasks.update_daily_statistics',
        'schedule': crontab(hour='*/1'),  # Chaque heure
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
