"""
Services pour intégrer les modules IA avec Django
"""

from django.core.cache import cache
from django.conf import settings
from apps.recommendations.models import ContentRecommendation, AIExplainability
from apps.emotions.models import EmotionDetection, EmotionalState, EmotionAdaptation
from apps.analytics.models import PerformanceMetric
from apps.content.models import Course
from .ai_engine import recommendation_engine, emotion_analyzer, difficulty_adapter
from .openai_service import openai_service
import logging

logger = logging.getLogger(__name__)


class RecommendationService:
    """Service pour générer et gérer les recommandations"""
    
    @staticmethod
    def generate_recommendations(user, limit=5):
        """
        Générer les recommandations personnalisées pour un utilisateur
        """
        try:
            # Récupérer les données utilisateur
            analytics = user.analytics
            performance_metrics = PerformanceMetric.objects.filter(user=user)
            
            # Construire le profil utilisateur
            user_profile = recommendation_engine.build_user_profile(
                user, analytics, performance_metrics
            )
            
            # Récupérer les cours disponibles
            courses_queryset = Course.objects.filter(status='published').values()
            courses = list(courses_queryset)
            
            # Convertir les résultats Django en dicts
            for i, course in enumerate(courses):
                course['id'] = str(course['id'])
            
            all_users = []  # À implémenter avec tous les utilisateurs
            
            # Générer les recommandations
            recommendations = []
            
            # Filtre collaboratif
            collab_recs = recommendation_engine.collaborative_filtering(user_profile, all_users, courses, k=3)
            recommendations.extend(collab_recs)
            
            # Filtre basé sur le contenu
            content_recs = recommendation_engine.content_based_filtering(user_profile, courses)
            recommendations.extend(content_recs)
            
            # Basé sur la performance
            perf_dict = {m.subject: {
                'success_rate': m.success_rate,
                'average_score': m.average_score,
                'difficulty_rating': m.difficulty_rating
            } for m in performance_metrics}
            
            if perf_dict:
                perf_recs = recommendation_engine.performance_based_recommendations(
                    user_profile, courses, perf_dict
                )
                recommendations.extend(perf_recs)
            
            # Personnaliser et limiter
            final_recommendations = recommendation_engine.personalize_recommendations(recommendations, k=limit)
            
            return final_recommendations
        
        except Exception as e:
            logger.error(f"Erreur dans la génération de recommandations: {e}")
            return []
    
    @staticmethod
    def save_recommendations(user, recommendations, limit: int = None):
        """
        Sauvegarder les recommandations en base de données.

        Génère une explication utilisateur via OpenAI lorsque possible et sauvegarde
        l'objet `AIExplainability` lié à la recommandation.
        """
        try:
            if not recommendations:
                return

            if limit is None:
                limit = len(recommendations)

            for i, rec in enumerate(recommendations):
                try:
                    # Résoudre l'id du contenu (varie selon la structure)
                    course_field = rec.get('course')
                    if isinstance(course_field, dict):
                        course_id = course_field.get('id')
                    else:
                        course_id = course_field

                    course = Course.objects.get(id=course_id)

                    # Préparer un contexte léger non sensible pour l'IA
                    user_context = {}
                    try:
                        if hasattr(user, 'learning_style'):
                            user_context['learning_style'] = getattr(user, 'learning_style')
                        elif hasattr(user, 'profile') and getattr(user.profile, 'learning_style', None):
                            user_context['learning_style'] = getattr(user.profile, 'learning_style')
                        if hasattr(user, 'analytics') and getattr(user.analytics, 'average_score', None) is not None:
                            user_context['recent_average'] = getattr(user.analytics, 'average_score')
                    except Exception:
                        user_context = {}

                    # Texte d'explication initial
                    explanation_text = rec.get('reason_text') or rec.get('reason')

                    # Appeler OpenAI pour générer une explication utilisateur si disponible
                    try:
                        rec_for_ai = {
                            'title': getattr(course, 'title', str(course)),
                            'reason': rec.get('reason'),
                            'factors': rec.get('factors', []),
                            'score': rec.get('score', 0.0),
                            'reason_text': rec.get('reason_text')
                        }

                        # Use caching to avoid repeated OpenAI calls
                        cache_key = None
                        ai_cached = None
                        try:
                            if getattr(settings, 'OPENAI_CACHE_ENABLED', True):
                                cache_key = f"openai:explanation:user:{user.id}:course:{getattr(course, 'id')}:{rec.get('reason')}:{int(rec.get('score', 0)*100)}"
                                ai_cached = cache.get(cache_key)
                        except Exception:
                            ai_cached = None

                        if ai_cached:
                            explanation_text = ai_cached
                        else:
                            ai_text = openai_service.generate_explanation(rec_for_ai, user_context=user_context)
                            if ai_text:
                                explanation_text = ai_text
                                try:
                                    if cache_key and getattr(settings, 'OPENAI_CACHE_ENABLED', True):
                                        ttl = getattr(settings, 'OPENAI_EXPLANATION_TTL', 86400)
                                        cache.set(cache_key, explanation_text, timeout=ttl)
                                except Exception:
                                    # don't break if cache set fails
                                    pass
                    except Exception:
                        # fallback to existing text
                        explanation_text = explanation_text

                    # Enregistrer la recommandation
                    content_rec = ContentRecommendation.objects.create(
                        user=user,
                        recommended_course=course,
                        reason=rec.get('reason'),
                        reason_explanation=explanation_text,
                        confidence_score=rec.get('score', 0.0),
                        priority=(limit - i),
                    )

                    # Enregistrer l'objet d'explicabilité IA
                    AIExplainability.objects.create(
                        recommendation=content_rec,
                        factors=rec.get('factors', {}),
                        primary_factor=rec.get('reason'),
                        primary_factor_contribution=rec.get('score', 0.0),
                        user_friendly_explanation=explanation_text,
                        supporting_data={'confidence': rec.get('score', 0.0), 'source': 'AI recommendation engine'},
                    )

                except Exception as e:
                    logger.error(f"Erreur en sauvegardant la recommandation pour {rec}: {e}")
        except Exception as e:
            logger.error(f"Erreur générale en sauvegardant les recommandations: {e}")


class EmotionService:
    """Service pour analyser et adapter selon les émotions"""
    
    @staticmethod
    def analyze_emotion_state(user):
        """
        Analyser l'état émotionnel agrégé de l'utilisateur
        """
        try:
            # Récupérer les détections émotionnelles récentes (24h)
            from django.utils import timezone
            from datetime import timedelta
            
            since = timezone.now() - timedelta(hours=24)
            emotion_history = EmotionDetection.objects.filter(
                user=user,
                created_at__gte=since
            ).values('detected_emotion', 'confidence').order_by('-created_at')
            
            # Analyser la tendance
            emotion_analysis = emotion_analyzer.analyze_emotion_trend(list(emotion_history))
            
            # Mettre à jour ou créer l'état émotionnel
            emotional_state, created = EmotionalState.objects.get_or_create(user=user)
            emotional_state.average_emotion = emotion_analysis['average_emotion']
            emotional_state.average_confidence = emotion_analysis['confidence']
            emotional_state.mood_trend = emotion_analysis['trend']
            emotional_state.stress_level = emotion_analysis['stress_level']
            emotional_state.engagement_level = emotion_analysis['engagement_level']
            emotional_state.fatigue_level = emotion_analysis['fatigue_level']
            emotional_state.save()
            
            return emotion_analysis
        
        except Exception as e:
            logger.error(f"Erreur lors de l'analyse émotionnelle: {e}")
            return {}
    
    @staticmethod
    def create_adaptation(user, emotion_detection, emotional_state):
        """
        Créer une adaptation basée sur l'état émotionnel
        """
        try:
            # Calculer l'adaptation
            adaptation_rec = emotion_analyzer.recommend_adaptation(emotional_state)
            
            if adaptation_rec['type']:
                # Créer la recommandation d'adaptation
                adaptation = EmotionAdaptation.objects.create(
                    user=user,
                    emotion_detection=emotion_detection,
                    adaptation_type=adaptation_rec['type'],
                    description=adaptation_rec['message'],
                    message_to_user=adaptation_rec['message'],
                    new_difficulty=adaptation_rec['settings'].get('difficulty'),
                    new_content_type=adaptation_rec['settings'].get('preferred_content_type')
                )
                
                return adaptation
        
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'adaptation: {e}")
            return None


class DifficultyAdaptationService:
    """Service pour adapter la difficulté des exercices"""
    
    @staticmethod
    def get_adaptive_difficulty(user, exercise):
        """
        Obtenir la difficulté adaptée pour un exercice
        """
        try:
            # Récupérer la performance de l'utilisateur sur cet exercice/sujet
            performance = PerformanceMetric.objects.filter(
                user=user,
                subject=exercise.difficulty_level
            ).first()
            
            if not performance:
                return exercise.difficulty_level
            
            # Récupérer l'état émotionnel si disponible
            try:
                emotional_state = user.emotional_state
                emotion_dict = {
                    'stress_level': emotional_state.stress_level,
                    'engagement_level': emotional_state.engagement_level,
                    'fatigue_level': emotional_state.fatigue_level
                }
            except:
                emotion_dict = None
            
            # Adapter la difficulté
            perf_dict = {
                'success_rate': performance.success_rate,
                'average_score': performance.average_score,
                'attempts': performance.total_attempts
            }
            
            new_difficulty = difficulty_adapter.calculate_adaptive_difficulty(
                perf_dict,
                exercise.difficulty_level,
                emotion_dict
            )
            
            return new_difficulty
        
        except Exception as e:
            logger.error(f"Erreur lors du calcul de difficulté adaptive: {e}")
            return exercise.difficulty_level
