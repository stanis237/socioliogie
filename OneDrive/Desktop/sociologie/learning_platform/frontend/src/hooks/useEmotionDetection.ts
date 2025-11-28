import { useState, useCallback, useRef, useEffect } from 'react';
import api from '../services/api';

export interface EmotionDetectionResult {
  emotion: string;
  confidence: number;
  timestamp: string;
}

export interface EmotionAnalytics {
  dominant_emotion: string;
  emotion_distribution: Record<string, number>;
  stress_index: number;
  engagement_index: number;
  fatigue_index: number;
  trend: 'improving' | 'stable' | 'declining';
}

export const useEmotionDetection = (enabled: boolean = true) => {
  const [isDetecting, setIsDetecting] = useState(false);
  const [isCapturing, setIsCapturing] = useState(false);
  const [detectionResult, setDetectionResult] = useState<EmotionDetectionResult | null>(null);
  const [analytics, setAnalytics] = useState<EmotionAnalytics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hasPermission, setHasPermission] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const captureIntervalRef = useRef<NodeJS.Timeout | null>(null);

  // Demander l'accès à la webcam
  const requestCameraPermission = useCallback(async (): Promise<boolean> => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640 },
          height: { ideal: 480 },
        },
        audio: false,
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        setHasPermission(true);
        return true;
      }
      return false;
    } catch (err: any) {
      setError(
        'Permission refusée: ' +
          (err.name === 'NotAllowedError'
            ? 'Veuillez autoriser l\'accès à la webcam'
            : 'Webcam non disponible')
      );
      return false;
    }
  }, []);

  // Capturer une frame et l'envoyer pour analyse
  const captureAndAnalyze = useCallback(async (): Promise<boolean> => {
    if (!canvasRef.current || !videoRef.current) {
      return false;
    }

    try {
      const context = canvasRef.current.getContext('2d');
      if (!context) return false;

      // Dessiner la vidéo sur le canvas
      canvasRef.current.width = videoRef.current.videoWidth;
      canvasRef.current.height = videoRef.current.videoHeight;
      context.drawImage(videoRef.current, 0, 0);

      // Convertir en blob
      return new Promise((resolve) => {
        canvasRef.current!.toBlob(async (blob) => {
          if (!blob) {
            resolve(false);
            return;
          }

          try {
            setIsDetecting(true);

            // Créer FormData avec l'image
            const formData = new FormData();
            formData.append('image', blob, 'emotion_frame.jpg');

            // Envoyer au serveur
            const response = await api.post<any>(
              '/emotions/detections/upload_emotion_data/',
              formData,
              {
                headers: {
                  'Content-Type': 'multipart/form-data',
                },
              }
            );

            if (response) {
              setDetectionResult({
                emotion: response.dominant_emotion,
                confidence: response.confidence_score,
                timestamp: new Date().toISOString(),
              });

              // Charger les analytics
              await loadEmotionAnalytics();
            }

            resolve(true);
          } catch (err: any) {
            console.error('Erreur lors de l\'analyse émotionnelle:', err);
            setError('Erreur lors de l\'analyse émotionnelle');
            resolve(false);
          } finally {
            setIsDetecting(false);
          }
        }, 'image/jpeg', 0.8);
      });
    } catch (err: any) {
      setError('Erreur lors de la capture');
      return false;
    }
  }, []);

  // Démarrer la capture continue
  const startCapturing = useCallback(async (): Promise<boolean> => {
    if (!hasPermission) {
      const granted = await requestCameraPermission();
      if (!granted) return false;
    }

    setIsCapturing(true);
    setError(null);

    // Capturer toutes les X secondes (défini dans les variables d'env)
    const interval = parseInt(
      process.env.REACT_APP_EMOTION_UPLOAD_INTERVAL || '5000'
    );

    captureIntervalRef.current = setInterval(() => {
      captureAndAnalyze();
    }, interval);

    // Première capture immédiatement
    await captureAndAnalyze();

    return true;
  }, [hasPermission, requestCameraPermission, captureAndAnalyze]);

  // Arrêter la capture
  const stopCapturing = useCallback(() => {
    setIsCapturing(false);

    if (captureIntervalRef.current) {
      clearInterval(captureIntervalRef.current);
      captureIntervalRef.current = null;
    }
  }, []);

  // Arrêter la webcam
  const stopCamera = useCallback(() => {
    stopCapturing();

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });
      streamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setHasPermission(false);
  }, [stopCapturing]);

  // Charger les analytics
  const loadEmotionAnalytics = useCallback(async (): Promise<EmotionAnalytics | null> => {
    try {
      const data = await api.get<EmotionAnalytics>(
        '/emotions/emotional-states/current/'
      );
      setAnalytics(data);
      return data;
    } catch (err: any) {
      console.error('Erreur lors du chargement des analytics:', err);
      return null;
    }
  }, []);

  // Nettoyer les ressources au démontage
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [stopCamera]);

  return {
    isDetecting,
    isCapturing,
    hasPermission,
    detectionResult,
    analytics,
    error,
    videoRef,
    canvasRef,
    requestCameraPermission,
    captureAndAnalyze,
    startCapturing,
    stopCapturing,
    stopCamera,
    loadEmotionAnalytics,
  };
};

// Hook pour formatter les résultats émotionnels
export const useEmotionFormatter = () => {
  const emotionEmojis: Record<string, string> = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    neutral: '😐',
    surprised: '😮',
    fearful: '😨',
    disgusted: '🤢',
    tired: '😴',
    focused: '🤓',
    confused: '😕',
  };

  const emotionColors: Record<string, string> = {
    happy: 'bg-yellow-100 text-yellow-800',
    sad: 'bg-blue-100 text-blue-800',
    angry: 'bg-red-100 text-red-800',
    neutral: 'bg-gray-100 text-gray-800',
    surprised: 'bg-purple-100 text-purple-800',
    fearful: 'bg-orange-100 text-orange-800',
    disgusted: 'bg-green-100 text-green-800',
    tired: 'bg-indigo-100 text-indigo-800',
    focused: 'bg-cyan-100 text-cyan-800',
    confused: 'bg-pink-100 text-pink-800',
  };

  const getEmoji = (emotion: string): string => emotionEmojis[emotion] || '😐';

  const getColor = (emotion: string): string => emotionColors[emotion] || 'bg-gray-100 text-gray-800';

  const getAdaptationAdvice = (emotion: string, stressLevel: number): string => {
    const adviceMap: Record<string, Record<string, string>> = {
      happy: {
        low: 'Excellent! Continuez à progresser à ce rythme optimal.',
        high: 'Vous êtes heureux mais stressé. Prenez une pause.',
      },
      sad: {
        low: 'Besoin de soutien. Essayez un exercice plus facile.',
        high: 'Vous vous sentez découragé. Prenez du repos et revenez plus tard.',
      },
      angry: {
        low: 'Restez calme. Prenez quelques respirations profondes.',
        high: 'Vous êtes trop stressé. Pause obligatoire recommandée.',
      },
      tired: {
        low: 'Un peu fatigué. Continuez avec un exercice léger.',
        high: 'Très fatigué. Pausez et revenez plus tard.',
      },
      focused: {
        low: 'Bon focus. Continuez votre session.',
        high: 'Hyper-concentré mais stressé. Ralentissez un peu.',
      },
      confused: {
        low: 'Confus mais motivé. Relisez la théorie.',
        high: 'Trop confus. Changez de sujet ou prenez une pause.',
      },
    };

    const advice = adviceMap[emotion];
    if (!advice) return 'Continuez à votre rythme!';

    return stressLevel > 0.6
      ? advice.high || 'Prenez une pause.'
      : advice.low || 'Continuez!';
  };

  return {
    getEmoji,
    getColor,
    getAdaptationAdvice,
  };
};
