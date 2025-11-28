import React, { useEffect, useState } from 'react';
import { useEmotionDetection, useEmotionFormatter } from '../hooks/useEmotionDetection';
import { useRecommendations } from '../hooks/useRecommendations';

const EmotionDetector: React.FC = () => {
  const {
    isCapturing,
    hasPermission,
    detectionResult,
    analytics,
    error,
    videoRef,
    canvasRef,
    requestCameraPermission,
    startCapturing,
    stopCapturing,
    stopCamera,
  } = useEmotionDetection(true);

  const { getEmoji, getColor, getAdaptationAdvice } = useEmotionFormatter();
  const { loadExerciseRecommendations } = useRecommendations();
  const [captureStatus, setCaptureStatus] = useState<string>('');

  useEffect(() => {
    if (isCapturing) {
      setCaptureStatus('Détection en cours...');
    } else if (hasPermission) {
      setCaptureStatus('Webcam prête');
    } else {
      setCaptureStatus('Webcam non autorisée');
    }
  }, [isCapturing, hasPermission]);

  const handleStart = async () => {
    const success = await requestCameraPermission();
    if (success) {
      await startCapturing();
    }
  };

  const handleAdaptCourse = async () => {
    if (detectionResult) {
      await loadExerciseRecommendations({
        emotion: detectionResult.emotion,
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Titre */}
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Détecteur d'Émotions Intelligent 🎭
        </h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Section Webcam */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Caméra en direct</h2>

            {/* Conteneur vidéo */}
            <div className="relative bg-gray-900 rounded-lg overflow-hidden mb-6" style={{ aspectRatio: '4/3' }}>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-full object-cover"
                style={{ display: hasPermission ? 'block' : 'none' }}
              />
              {!hasPermission && (
                <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
                  <div className="text-center">
                    <p className="text-gray-400 text-lg mb-4">📹 Webcam non autorisée</p>
                    <button
                      onClick={handleStart}
                      className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
                    >
                      Autoriser la webcam
                    </button>
                  </div>
                </div>
              )}
              <canvas ref={canvasRef} className="hidden" />

              {/* Indicateur d'état */}
              <div className="absolute top-4 right-4">
                <span
                  className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    isCapturing
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  <span className={`h-2 w-2 rounded-full mr-2 ${isCapturing ? 'bg-green-600 animate-pulse' : 'bg-gray-600'}`} />
                  {captureStatus}
                </span>
              </div>
            </div>

            {/* Boutons de contrôle */}
            <div className="flex gap-4 justify-center mb-6">
              {!isCapturing ? (
                <button
                  onClick={handleStart}
                  disabled={!hasPermission}
                  className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition font-medium"
                >
                  Démarrer la détection
                </button>
              ) : (
                <button
                  onClick={stopCapturing}
                  className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition font-medium"
                >
                  Arrêter la détection
                </button>
              )}

              {hasPermission && (
                <button
                  onClick={stopCamera}
                  className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition font-medium"
                >
                  Fermer la webcam
                </button>
              )}
            </div>

            {/* Message d'erreur */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700 mb-6">
                {error}
              </div>
            )}
          </div>

          {/* Résultats */}
          <div className="space-y-6">
            {/* Détection actuelle */}
            {detectionResult && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Détection actuelle</h3>

                <div className="text-center py-6">
                  <div className="text-6xl mb-4">{getEmoji(detectionResult.emotion)}</div>
                  <div className={`inline-block px-4 py-2 rounded-lg font-semibold ${getColor(detectionResult.emotion)}`}>
                    {detectionResult.emotion.charAt(0).toUpperCase() + detectionResult.emotion.slice(1)}
                  </div>
                </div>

                <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                  <p className="text-sm text-gray-700">
                    <strong>Confiance:</strong> {(detectionResult.confidence * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-gray-600 mt-2">
                    Détecté: {new Date(detectionResult.timestamp).toLocaleTimeString('fr-FR')}
                  </p>
                </div>

                {/* Conseil d'adaptation */}
                {analytics && (
                  <div className="mt-4 p-4 bg-amber-50 rounded-lg border-l-4 border-amber-400">
                    <p className="text-sm font-medium text-amber-900">
                      💡 {getAdaptationAdvice(detectionResult.emotion, analytics.stress_index)}
                    </p>
                  </div>
                )}

                <button
                  onClick={handleAdaptCourse}
                  className="w-full mt-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition font-medium text-sm"
                >
                  Adapter le cours
                </button>
              </div>
            )}

            {/* Analytics */}
            {analytics && (
              <div className="bg-white rounded-xl shadow-lg p-6">
                <h3 className="text-lg font-bold text-gray-900 mb-4">Analyse émotionnelle</h3>

                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">Stress</span>
                      <span className="text-sm font-semibold text-red-600">
                        {(analytics.stress_index * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-red-500 h-2 rounded-full transition-all"
                        style={{ width: `${analytics.stress_index * 100}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">Concentration</span>
                      <span className="text-sm font-semibold text-green-600">
                        {(analytics.engagement_index * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full transition-all"
                        style={{ width: `${analytics.engagement_index * 100}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-sm font-medium text-gray-700">Fatigue</span>
                      <span className="text-sm font-semibold text-yellow-600">
                        {(analytics.fatigue_index * 100).toFixed(0)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-yellow-500 h-2 rounded-full transition-all"
                        style={{ width: `${analytics.fatigue_index * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-xs text-gray-600">
                    <strong>État dominant:</strong> {analytics.dominant_emotion}
                  </p>
                  <p className="text-xs text-gray-600 mt-1">
                    <strong>Tendance:</strong> {analytics.trend === 'improving' ? '📈 Amélioration' : analytics.trend === 'stable' ? '➡️ Stable' : '📉 Déclin'}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default EmotionDetector;
