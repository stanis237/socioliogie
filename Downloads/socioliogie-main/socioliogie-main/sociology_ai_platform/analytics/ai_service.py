"""
Services d'intelligence artificielle pour la plateforme
- Reconnaissance d'émotion
- Recommandations personnalisées
- Analyse de l'état d'apprentissage
"""
import random
from django.db.models import Avg, Count, Q
from .models import Recommendation, EmotionData
from content.models import Course
from accounts.models import Historique, UserProfile


class EmotionRecognitionService:
    """Service de reconnaissance et d'analyse des émotions"""
    
    @staticmethod
    def analyze_learning_state(user):
        """
        Analyse l'état d'apprentissage de l'utilisateur basé sur ses émotions récentes
        Retourne un dictionnaire avec l'état d'apprentissage
        """
        recent_emotions = EmotionData.objects.filter(user=user).order_by('-recorded_at')[:10]
        
        if not recent_emotions.exists():
            return {
                'state': 'unknown',
                'optimal_time': False,
                'suggested_action': 'Commencer à apprendre',
                'mood': 'neutral'
            }
        
        # Calculer la moyenne des intensités
        avg_intensity = recent_emotions.aggregate(Avg('intensity'))['intensity__avg'] or 0.5
        
        # Analyser les types d'émotions les plus fréquents
        emotion_counts = {}
        for emotion in recent_emotions:
            emotion_counts[emotion.emotion_type] = emotion_counts.get(emotion.emotion_type, 0) + 1
        
        dominant_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else 'neutral'
        
        # Déterminer l'état d'apprentissage optimal
        optimal_emotions = ['focused', 'excited', 'happy']
        optimal_time = dominant_emotion in optimal_emotions and avg_intensity > 0.6
        
        # Suggestions basées sur l'émotion dominante
        suggestions = {
            'happy': 'C\'est le moment idéal pour apprendre de nouveaux concepts!',
            'focused': 'Vous êtes concentré, profitez-en pour approfondir vos connaissances.',
            'excited': 'Votre enthousiasme est parfait pour explorer de nouveaux sujets!',
            'confused': 'Prenez une pause ou revoyez les concepts de base.',
            'sad': 'Essayez un contenu plus léger ou prenez une pause.',
            'neutral': 'Commencez par du contenu qui vous intéresse.'
        }
        
        return {
            'state': dominant_emotion,
            'optimal_time': optimal_time,
            'suggested_action': suggestions.get(dominant_emotion, 'Continuez votre apprentissage'),
            'mood': dominant_emotion,
            'intensity': avg_intensity,
            'recent_count': recent_emotions.count()
        }
    
    @staticmethod
    def recognize_emotion_from_face(face_data):
        """
        Simule la reconnaissance d'émotion à partir de données faciales
        Dans une implémentation réelle, cela utiliserait OpenCV, TensorFlow, ou une API
        """
        # Simulation basique - dans la réalité, cela utiliserait un modèle ML
        emotions = ['happy', 'sad', 'neutral', 'focused', 'confused', 'excited']
        # Simuler une détection basée sur des caractéristiques faciales
        detected_emotion = random.choice(emotions)
        confidence = random.uniform(0.6, 0.95)
        
        return {
            'emotion': detected_emotion,
            'confidence': confidence,
            'intensity': confidence
        }


class AIRecommendationService:
    """Service de recommandation basé sur l'IA"""
    
    @staticmethod
    def generate_recommendations(user, limit=5):
        """
        Génère des recommandations personnalisées pour l'utilisateur
        Basé sur:
        - Historique d'apprentissage
        - Niveau de l'utilisateur
        - Émotions récentes
        - Cours non complétés
        """
        profile = user.profile
        completed_courses = Historique.objects.filter(
            user=user, 
            content_type='course', 
            completed=True
        ).values_list('content_id', flat=True)
        
        # Obtenir les cours non complétés
        available_courses = Course.objects.exclude(id__in=completed_courses)
        
        if not available_courses.exists():
            return []
        
        # Analyser l'état d'apprentissage
        learning_state = EmotionRecognitionService.analyze_learning_state(user)
        
        recommendations = []
        for course in available_courses:
            score = AIRecommendationService._calculate_recommendation_score(
                user, course, profile, learning_state
            )
            
            # Créer ou mettre à jour la recommandation
            recommendation, created = Recommendation.objects.update_or_create(
                user=user,
                course=course,
                defaults={
                    'score': score,
                    'reason': AIRecommendationService._generate_reason(
                        course, profile, learning_state, score
                    ),
                    'viewed': False
                }
            )
            recommendations.append(recommendation)
        
        # Trier par score et retourner les meilleures
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]
    
    @staticmethod
    def _calculate_recommendation_score(user, course, profile, learning_state):
        """
        Calcule un score de recommandation (0-1) pour un cours
        """
        score = 0.5  # Score de base
        
        # Facteur 1: Niveau de l'utilisateur
        level_scores = {
            'beginner': 0.3,
            'intermediate': 0.5,
            'advanced': 0.7
        }
        score += level_scores.get(profile.level, 0.5) * 0.2
        
        # Facteur 2: État émotionnel optimal
        if learning_state.get('optimal_time', False):
            score += 0.2
        
        # Facteur 3: Popularité du cours (basé sur le nombre de recommandations)
        course_recommendations = Recommendation.objects.filter(course=course).count()
        popularity_factor = min(course_recommendations / 10, 0.1)  # Max 0.1
        score += popularity_factor
        
        # Facteur 4: Nouveauté (cours récents)
        from django.utils import timezone
        from datetime import timedelta
        days_old = (timezone.now() - course.created_at).days
        if days_old < 30:
            score += 0.1
        
        # Normaliser entre 0 et 1
        score = min(score, 1.0)
        score = max(score, 0.0)
        
        # Ajouter un peu de randomisation pour la variété
        score += random.uniform(-0.05, 0.05)
        score = min(score, 1.0)
        score = max(score, 0.0)
        
        return round(score, 3)
    
    @staticmethod
    def _generate_reason(course, profile, learning_state, score):
        """
        Génère une raison textuelle pour la recommandation
        """
        reasons = []
        
        if learning_state.get('optimal_time', False):
            reasons.append("Moment optimal pour apprendre")
        
        if profile.level == 'beginner' and score > 0.6:
            reasons.append("Parfait pour débuter")
        elif profile.level == 'advanced' and score > 0.7:
            reasons.append("Contenu avancé adapté à votre niveau")
        
        if score > 0.8:
            reasons.append("Recommandation personnalisée")
        
        if not reasons:
            reasons.append("Basé sur vos préférences d'apprentissage")
        
        return " | ".join(reasons)
    
    @staticmethod
    def adapt_content_difficulty(user, course):
        """
        Adapte la difficulté du contenu selon le profil de l'utilisateur
        """
        profile = user.profile
        recent_emotions = EmotionData.objects.filter(user=user).order_by('-recorded_at')[:5]
        
        # Si l'utilisateur est confus, suggérer du contenu plus facile
        if recent_emotions.exists():
            avg_intensity = recent_emotions.aggregate(Avg('intensity'))['intensity__avg'] or 0.5
            confused_count = recent_emotions.filter(emotion_type='confused').count()
            
            if confused_count > 2 or avg_intensity < 0.3:
                return 'easy'
        
        # Sinon, utiliser le niveau du profil
        level_mapping = {
            'beginner': 'easy',
            'intermediate': 'medium',
            'advanced': 'hard'
        }
        return level_mapping.get(profile.level, 'medium')
    
    @staticmethod
    def get_courses_by_emotion(user, emotion_type, limit=5):
        """
        Retourne des cours recommandés basés sur l'émotion détectée
        """
        completed_courses = Historique.objects.filter(
            user=user, 
            content_type='course', 
            completed=True
        ).values_list('content_id', flat=True)
        
        # Obtenir les cours non complétés
        available_courses = Course.objects.exclude(id__in=completed_courses)
        
        if not available_courses.exists():
            return []
        
        # Mapping émotion -> difficulté recommandée
        emotion_to_difficulty = {
            'happy': ['beginner', 'intermediate', 'advanced'],  # Tous les niveaux
            'excited': ['intermediate', 'advanced'],  # Contenu stimulant
            'focused': ['intermediate', 'advanced'],  # Contenu approfondi
            'neutral': ['beginner', 'intermediate'],  # Contenu standard
            'confused': ['beginner'],  # Contenu de base
            'sad': ['beginner'],  # Contenu léger
        }
        
        # Obtenir les difficultés recommandées pour cette émotion
        recommended_difficulties = emotion_to_difficulty.get(emotion_type, ['beginner', 'intermediate'])
        
        # Filtrer les cours par difficulté recommandée
        recommended_courses = available_courses.filter(difficulty__in=recommended_difficulties)
        
        # Si pas assez de cours, inclure tous les cours disponibles
        if recommended_courses.count() < limit:
            recommended_courses = available_courses
        
        # Générer des recommandations avec scores
        recommendations = []
        for course in recommended_courses[:limit * 2]:  # Prendre plus pour trier
            score = AIRecommendationService._calculate_emotion_based_score(
                course, emotion_type, recommended_difficulties
            )
            
            # Créer ou mettre à jour la recommandation
            recommendation, created = Recommendation.objects.update_or_create(
                user=user,
                course=course,
                defaults={
                    'score': score,
                    'reason': AIRecommendationService._generate_emotion_reason(emotion_type, course),
                    'viewed': False
                }
            )
            recommendations.append(recommendation)
        
        # Trier par score et retourner les meilleures
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]
    
    @staticmethod
    def _calculate_emotion_based_score(course, emotion_type, recommended_difficulties):
        """
        Calcule un score basé sur l'émotion et la difficulté du cours
        """
        score = 0.5  # Score de base
        
        # Bonus si la difficulté correspond à l'émotion
        if course.difficulty in recommended_difficulties:
            score += 0.3
        
        # Bonus selon l'émotion
        emotion_bonus = {
            'happy': 0.2,
            'excited': 0.25,
            'focused': 0.2,
            'neutral': 0.1,
            'confused': 0.15,
            'sad': 0.1,
        }
        score += emotion_bonus.get(emotion_type, 0.1)
        
        # Normaliser
        score = min(score, 1.0)
        score = max(score, 0.0)
        
        return round(score, 3)
    
    @staticmethod
    def _generate_emotion_reason(emotion_type, course):
        """
        Génère une raison basée sur l'émotion détectée
        """
        emotion_reasons = {
            'happy': f'Parfait pour votre état positif ! Ce cours {course.get_difficulty_display().lower()} vous conviendra.',
            'excited': f'Votre enthousiasme est idéal pour ce cours {course.get_difficulty_display().lower()} !',
            'focused': f'Vous êtes concentré, profitez-en pour approfondir avec ce cours {course.get_difficulty_display().lower()}.',
            'neutral': f'Ce cours {course.get_difficulty_display().lower()} est adapté à votre état actuel.',
            'confused': f'Nous vous recommandons ce cours {course.get_difficulty_display().lower()} pour clarifier les concepts.',
            'sad': f'Ce cours {course.get_difficulty_display().lower()} est conçu pour être accessible et motivant.',
        }
        
        return emotion_reasons.get(emotion_type, f'Cours recommandé basé sur votre état émotionnel.')
