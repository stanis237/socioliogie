"""
Module d'Intelligence Artificielle pour la plateforme d'apprentissage personnalisé
"""

import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """
    Moteur de recommandation basé sur les algorithmes collaboratifs et contentbased
    """
    
    def __init__(self):
        self.user_profiles = {}
        self.content_vectors = {}
        self.scaler = StandardScaler()
    
    def build_user_profile(self, user, analytics, performance_metrics):
        """
        Construire un profil utilisateur complet
        """
        profile = {
            'user_id': str(user.id),
            'learning_style': user.learning_style,
            'proficiency_level': user.proficiency_level,
            'interests': user.interests,
            'goals': user.goals,
            'total_learning_time': analytics.total_learning_time,
            'average_exercise_score': analytics.average_exercise_score,
            'learning_consistency': analytics.learning_consistency,
            'motivation_level': analytics.motivation_level,
            'current_streak': analytics.current_streak,
        }
        
        # Ajouter les métriques de performance
        if performance_metrics:
            profile['performance'] = {
                metric.subject: {
                    'success_rate': metric.success_rate,
                    'average_score': metric.average_score,
                    'difficulty_rating': metric.difficulty_rating,
                } for metric in performance_metrics
            }
        
        return profile
    
    def collaborative_filtering(self, user_profile: Dict, all_users: List[Dict], 
                               courses: List[Dict], k: int = 5) -> List[Tuple]:
        """
        Filtre collaboratif - recommander basé sur utilisateurs similaires
        """
        recommendations = []
        
        # Extraire les features numériques
        if not all_users or not courses:
            return recommendations
        
        # Trouver les utilisateurs similaires
        similar_users = self._find_similar_users(user_profile, all_users, k)
        
        # Collecter les contenus appréciés par les utilisateurs similaires
        for similar_user, similarity_score in similar_users:
            for course in courses:
                if self._user_completed(similar_user, course):
                    recommendations.append({
                        'course': course,
                        'score': similarity_score * 0.8,  # Pondérer par similarité
                        'reason': 'similar_users',
                        'reason_text': f"Les utilisateurs ayant un profil similaire au vôtre ont apprécié ce cours."
                    })
        
        return recommendations
    
    def content_based_filtering(self, user_profile: Dict, courses: List[Dict]) -> List[Dict]:
        """
        Filtrage basé sur le contenu
        """
        recommendations = []
        
        for course in courses:
            # Vérifier la correspondance avec les intérêts
            interest_match = self._calculate_interest_match(user_profile['interests'], course.get('tags', []))
            
            # Vérifier la correspondance avec le niveau de profondeur
            difficulty_match = self._calculate_difficulty_match(
                user_profile['proficiency_level'],
                course.get('difficulty_level')
            )
            
            # Vérifier les prérequis
            prerequisites_met = self._check_prerequisites(user_profile, course.get('prerequisites', []))
            
            if interest_match > 0.3 and prerequisites_met:
                score = (interest_match * 0.5) + (difficulty_match * 0.5)
                recommendations.append({
                    'course': course,
                    'score': score,
                    'reason': 'learning_style',
                    'reason_text': f"Ce cours correspond à vos intérêts ({interest_match:.0%}) et votre niveau.",
                    'interest_match': interest_match,
                    'difficulty_match': difficulty_match
                })
        
        return recommendations
    
    def performance_based_recommendations(self, user_profile: Dict, courses: List[Dict],
                                         performance_metrics: Dict) -> List[Dict]:
        """
        Recommandations basées sur la performance
        """
        recommendations = []
        
        for subject, metrics in performance_metrics.items():
            # Identifier les faiblesses
            if metrics['success_rate'] < 0.7:
                # Recommander des cours de renforcement
                for course in courses:
                    if subject in course.get('tags', []) and course.get('difficulty_level') != 'hard':
                        recommendations.append({
                            'course': course,
                            'score': 0.85,
                            'reason': 'performance',
                            'reason_text': f"Vous avez eu une réussite de {metrics['success_rate']:.0%} en {subject}. Ce cours peut vous aider."
                        })
        
        return recommendations
    
    def emotional_state_based_recommendations(self, emotional_state: Dict, courses: List[Dict]) -> List[Dict]:
        """
        Recommandations basées sur l'état émotionnel
        """
        recommendations = []
        
        stress_level = emotional_state.get('stress_level', 50)
        engagement = emotional_state.get('engagement_level', 50)
        
        for course in courses:
            if stress_level > 70:
                # Recommander des contenus relaxants avec vidéos et explications détaillées
                if course.get('content_type') in ['video', 'article']:
                    recommendations.append({
                        'course': course,
                        'score': 0.7,
                        'reason': 'emotional_state',
                        'reason_text': "Nous avons détecté du stress. Ce contenu audiovisuel peut vous aider à vous relaxer."
                    })
            
            elif engagement < 40:
                # Recommander du contenu interactif
                if course.get('content_type') == 'interactive':
                    recommendations.append({
                        'course': course,
                        'score': 0.8,
                        'reason': 'emotional_state',
                        'reason_text': "Nous recommandons du contenu interactif pour améliorer votre engagement."
                    })
        
        return recommendations
    
    def personalize_recommendations(self, recommendations: List[Dict], k: int = 5) -> List[Dict]:
        """
        Personnaliser et classer les recommandations finales
        """
        # Trier par score
        sorted_recs = sorted(recommendations, key=lambda x: x.get('score', 0), reverse=True)
        
        # Retirer les doublons
        seen = set()
        unique_recs = []
        for rec in sorted_recs:
            course_id = rec['course'].get('id')
            if course_id not in seen:
                unique_recs.append(rec)
                seen.add(course_id)
            if len(unique_recs) >= k:
                break
        
        return unique_recs
    
    def _find_similar_users(self, user_profile: Dict, all_users: List[Dict], k: int) -> List[Tuple]:
        """Trouver les k utilisateurs les plus similaires"""
        # Implémentation simplifiée
        similar = []
        for other_user in all_users:
            if other_user['user_id'] != user_profile['user_id']:
                similarity = self._calculate_user_similarity(user_profile, other_user)
                similar.append((other_user, similarity))
        
        return sorted(similar, key=lambda x: x[1], reverse=True)[:k]
    
    def _calculate_user_similarity(self, user1: Dict, user2: Dict) -> float:
        """Calculer la similarité entre deux utilisateurs"""
        score = 0
        
        # Learning style
        if user1.get('learning_style') == user2.get('learning_style'):
            score += 0.3
        
        # Proficiency level
        if user1.get('proficiency_level') == user2.get('proficiency_level'):
            score += 0.2
        
        # Intérêts communs
        interests1 = set(user1.get('interests', []))
        interests2 = set(user2.get('interests', []))
        if interests1 and interests2:
            common = len(interests1 & interests2)
            score += (common / len(interests1 | interests2)) * 0.3
        
        # Performance moyenne
        perf1 = user1.get('average_exercise_score', 0)
        perf2 = user2.get('average_exercise_score', 0)
        if perf1 and perf2:
            diff = abs(perf1 - perf2) / 100
            score += (1 - diff) * 0.2
        
        return min(score, 1.0)
    
    def _calculate_interest_match(self, user_interests: List[str], course_tags: List[str]) -> float:
        """Calculer le pourcentage de correspondance des intérêts"""
        if not user_interests or not course_tags:
            return 0
        
        user_set = set(user_interests)
        course_set = set(course_tags)
        
        intersection = len(user_set & course_set)
        union = len(user_set | course_set)
        
        return intersection / union if union > 0 else 0
    
    def _calculate_difficulty_match(self, user_level: str, course_level: str) -> float:
        """Calculer la correspondance du niveau de difficulté"""
        levels = ['beginner', 'intermediate', 'advanced', 'expert']
        
        if user_level not in levels or course_level not in levels:
            return 0.5
        
        user_idx = levels.index(user_level)
        course_idx = levels.index(course_level)
        
        # Score maximal si le niveau est approprié
        diff = abs(user_idx - course_idx)
        return max(0, 1 - (diff * 0.25))
    
    def _check_prerequisites(self, user_profile: Dict, prerequisites: List) -> bool:
        """Vérifier si les prérequis sont respectés"""
        if not prerequisites:
            return True
        
        # À implémenter: vérifier si l'utilisateur a complété les cours prérequis
        return True
    
    def _user_completed(self, user: Dict, course: Dict) -> bool:
        """Vérifier si un utilisateur a complété un cours"""
        # À implémenter avec la BD
        return False


class EmotionAnalyzer:
    """
    Analyseur d'émotions et adaptation du parcours
    """
    
    EMOTION_INTENSITY = {
        'happy': 0.9,
        'focused': 0.8,
        'neutral': 0.5,
        'confused': 0.4,
        'tired': 0.2,
        'stressed': 0.1,
        'angry': 0.0,
    }
    
    def analyze_emotion_trend(self, emotion_history: List[Dict]) -> Dict:
        """
        Analyser la tendance des émotions
        """
        if not emotion_history:
            return {
                'trend': 'no_data',
                'average_emotion': None,
                'stress_level': 50,
                'engagement_level': 50,
                'fatigue_level': 50,
            }
        
        emotions = [e['detected_emotion'] for e in emotion_history]
        confidences = [e['confidence'] for e in emotion_history]
        
        # Calculer les indices
        stress_index = self._calculate_stress_index(emotions)
        engagement_index = self._calculate_engagement_index(emotions)
        fatigue_index = self._calculate_fatigue_index(emotions)
        
        # Déterminer la tendance
        if len(emotion_history) > 1:
            recent = emotion_history[-5:]
            trend_direction = self._calculate_trend(recent)
        else:
            trend_direction = 'stable'
        
        return {
            'trend': trend_direction,
            'average_emotion': max(set(emotions), key=emotions.count),
            'stress_level': stress_index,
            'engagement_level': engagement_index,
            'fatigue_level': fatigue_index,
            'confidence': np.mean(confidences),
        }
    
    def recommend_adaptation(self, emotion_state: Dict) -> Dict:
        """
        Recommander une adaptation basée sur l'état émotionnel
        """
        stress = emotion_state.get('stress_level', 50)
        engagement = emotion_state.get('engagement_level', 50)
        fatigue = emotion_state.get('fatigue_level', 50)
        
        adaptation = {
            'type': None,
            'message': '',
            'settings': {}
        }
        
        # Règles d'adaptation
        if stress > 75:
            adaptation['type'] = 'break'
            adaptation['message'] = "Nous avons détecté du stress élevé. Une pause est recommandée."
            adaptation['settings']['break_duration'] = 15
        
        elif fatigue > 75:
            adaptation['type'] = 'break'
            adaptation['message'] = "Vous semblez fatigué. Reposez-vous quelques minutes."
            adaptation['settings']['break_duration'] = 10
        
        elif engagement < 30:
            adaptation['type'] = 'change_content'
            adaptation['message'] = "Changeons de type de contenu pour augmenter votre engagement."
            adaptation['settings']['preferred_content_type'] = 'interactive'
        
        elif stress > 50:
            adaptation['type'] = 'difficulty_adjust'
            adaptation['message'] = "Nous ajustons la difficulté pour réduire votre stress."
            adaptation['settings']['difficulty'] = 'easy'
        
        return adaptation
    
    def _calculate_stress_index(self, emotions: List[str]) -> float:
        """Calculer un indice de stress (0-100)"""
        stress_emotions = {'angry': 80, 'confused': 60, 'fearful': 70}
        
        if not emotions:
            return 50
        
        stress_scores = [stress_emotions.get(e, 0) for e in emotions]
        return np.mean(stress_scores) if stress_scores else 50
    
    def _calculate_engagement_index(self, emotions: List[str]) -> float:
        """Calculer un indice d'engagement (0-100)"""
        engagement_emotions = {'focused': 90, 'happy': 80, 'surprised': 70}
        
        if not emotions:
            return 50
        
        engagement_scores = [engagement_emotions.get(e, 30) for e in emotions]
        return np.mean(engagement_scores) if engagement_scores else 50
    
    def _calculate_fatigue_index(self, emotions: List[str]) -> float:
        """Calculer un indice de fatigue (0-100)"""
        fatigue_emotions = {'tired': 80, 'sad': 50, 'neutral': 40}
        
        if not emotions:
            return 50
        
        fatigue_scores = [fatigue_emotions.get(e, 0) for e in emotions]
        return np.mean(fatigue_scores) if fatigue_scores else 50
    
    def _calculate_trend(self, recent_emotions: List[Dict]) -> str:
        """Calculer la tendance des émotions récentes"""
        if len(recent_emotions) < 2:
            return 'stable'
        
        # Calculer les scores d'intensité
        scores = [self.EMOTION_INTENSITY.get(e['detected_emotion'], 0.5) 
                 for e in recent_emotions]
        
        # Calculer la pente
        if len(scores) >= 2:
            trend = np.polyfit(range(len(scores)), scores, 1)[0]
            
            if trend > 0.1:
                return 'improving'
            elif trend < -0.1:
                return 'declining'
        
        return 'stable'


class ExerciseDifficultyAdapter:
    """
    Adaptation dynamique de la difficulté des exercices
    """
    
    def calculate_adaptive_difficulty(self, user_performance: Dict, 
                                     current_difficulty: str,
                                     emotional_state: Dict = None) -> str:
        """
        Calculer la difficulté adaptée basée sur la performance
        """
        success_rate = user_performance.get('success_rate', 0)
        average_score = user_performance.get('average_score', 0)
        attempts = user_performance.get('attempts', 1)
        
        # Calculer un score adaptatif
        adaptive_score = (success_rate * 0.5) + ((average_score / 100) * 0.5)
        
        difficulty_levels = ['easy', 'medium', 'hard']
        current_idx = difficulty_levels.index(current_difficulty) if current_difficulty in difficulty_levels else 1
        
        # Ajuster en fonction de la performance
        if adaptive_score > 0.85:
            # Augmenter la difficulté
            new_idx = min(current_idx + 1, len(difficulty_levels) - 1)
        elif adaptive_score < 0.5:
            # Diminuer la difficulté
            new_idx = max(current_idx - 1, 0)
        else:
            # Garder la même difficulté
            new_idx = current_idx
        
        # Ajuster selon l'état émotionnel
        if emotional_state and emotional_state.get('stress_level', 50) > 70:
            new_idx = max(new_idx - 1, 0)
        
        return difficulty_levels[new_idx]


# Instance globale
recommendation_engine = RecommendationEngine()
emotion_analyzer = EmotionAnalyzer()
difficulty_adapter = ExerciseDifficultyAdapter()
