import { useState, useCallback, useEffect } from 'react';
import api from '../services/api';

export interface Recommendation {
  id: number;
  content_id: number;
  content_title: string;
  content_type: 'course' | 'module' | 'lesson';
  confidence_score: number;
  reason: string;
  reason_text: string;
  factors: RecommendationFactor[];
  created_at: string;
}

export interface RecommendationFactor {
  name: string;
  weight: number;
  value: number;
  explanation: string;
}

export interface ExerciseRecommendation {
  id: number;
  exercise_id: number;
  exercise_title: string;
  difficulty_level: 'easy' | 'medium' | 'hard';
  confidence_score: number;
  reason: string;
  created_at: string;
}

export interface EmotionState {
  id: number;
  dominant_emotion: string;
  emotion_scores: Record<string, number>;
  stress_level: number;
  engagement_level: number;
  fatigue_level: number;
  created_at: string;
}

export const useRecommendations = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [exerciseRecommendations, setExerciseRecommendations] = useState<
    ExerciseRecommendation[]
  >([]);
  const [emotionState, setEmotionState] = useState<EmotionState | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Charger les recommandations de contenu
  const loadRecommendations = useCallback(async (params?: any) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await api.get<{
        results: Recommendation[];
        count: number;
      }>('/recommendations/content-recommendations/', { params });

      setRecommendations(data.results);
      return data.results;
    } catch (err: any) {
      setError('Erreur lors du chargement des recommandations');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Charger les recommandations d'exercices
  const loadExerciseRecommendations = useCallback(async (params?: any) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await api.get<{
        results: ExerciseRecommendation[];
        count: number;
      }>('/recommendations/exercise-recommendations/', { params });

      setExerciseRecommendations(data.results);
      return data.results;
    } catch (err: any) {
      setError('Erreur lors du chargement des recommandations d\'exercices');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Charger l'état émotionnel actuel
  const loadEmotionState = useCallback(async () => {
    setIsLoading(true);

    try {
      const data = await api.get<EmotionState>(
        '/emotions/emotional-states/current/'
      );
      setEmotionState(data);
      return data;
    } catch (err: any) {
      console.error('Erreur lors du chargement de l\'état émotionnel:', err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Envoyer un feedback sur une recommandation
  const sendFeedback = useCallback(
    async (
      recommendationId: number,
      helpful: boolean,
      reason?: string
    ): Promise<boolean> => {
      try {
        await api.post(`/recommendations/content-recommendations/${recommendationId}/feedback/`, {
          is_helpful: helpful,
          feedback_reason: reason,
        });
        return true;
      } catch (err: any) {
        console.error('Erreur lors de l\'envoi du feedback:', err);
        return false;
      }
    },
    []
  );

  // Générer de nouvelles recommandations
  const generateRecommendations = useCallback(async (): Promise<boolean> => {
    setIsLoading(true);

    try {
      await api.post('/recommendations/generate/', {});
      await loadRecommendations();
      await loadExerciseRecommendations();
      return true;
    } catch (err: any) {
      setError('Erreur lors de la génération des recommandations');
      console.error(err);
      return false;
    } finally {
      setIsLoading(false);
    }
  }, [loadRecommendations, loadExerciseRecommendations]);

  return {
    recommendations,
    exerciseRecommendations,
    emotionState,
    isLoading,
    error,
    loadRecommendations,
    loadExerciseRecommendations,
    loadEmotionState,
    sendFeedback,
    generateRecommendations,
  };
};

// Hook pour afficher les explications IA de manière lisible
export const useAIExplanation = (factors: RecommendationFactor[]) => {
  const formatExplanation = useCallback(() => {
    if (!factors || factors.length === 0) {
      return 'Aucune explication disponible';
    }

    return factors
      .sort((a, b) => b.weight - a.weight)
      .map((factor) => `${factor.explanation} (poids: ${(factor.weight * 100).toFixed(0)}%)`)
      .join(' | ');
  }, [factors]);

  const getTopFactors = useCallback((limit: number = 3) => {
    return factors
      .sort((a, b) => b.weight - a.weight)
      .slice(0, limit);
  }, [factors]);

  return {
    formatExplanation,
    getTopFactors,
  };
};
