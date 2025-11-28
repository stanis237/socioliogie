import React, { useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useRecommendations } from '../hooks/useRecommendations';
import { useEmotionDetection } from '../hooks/useEmotionDetection';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Navigate } from 'react-router-dom';

interface DashboardStats {
  courses_completed: number;
  current_streak: number;
  total_hours: number;
  average_score: number;
}

const Dashboard: React.FC = () => {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const { recommendations, emotionState, loadRecommendations, loadEmotionState } =
    useRecommendations();
  const { analytics, loadEmotionAnalytics } = useEmotionDetection(false);
  const [stats, setStats] = React.useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = React.useState(true);

  useEffect(() => {
    if (!isAuthenticated) return;

    const loadDashboard = async () => {
      try {
        await Promise.all([
          loadRecommendations({ limit: 5 }),
          loadEmotionState(),
          loadEmotionAnalytics(),
        ]);

        // Simulé pour l'exemple - à remplacer par vraie API
        setStats({
          courses_completed: 3,
          current_streak: 7,
          total_hours: 24.5,
          average_score: 82,
        });
      } catch (error) {
        console.error('Erreur lors du chargement du dashboard:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboard();
  }, [isAuthenticated, loadRecommendations, loadEmotionState, loadEmotionAnalytics]);

  if (authLoading || isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // Le dashboard est maintenant public - pas de redirection

  // Données fictives pour les graphiques
  const progressData = [
    { month: 'Jan', score: 65 },
    { month: 'Fév', score: 72 },
    { month: 'Mar', score: 78 },
    { month: 'Avr', score: 82 },
    { month: 'Mai', score: 88 },
    { month: 'Jun', score: 92 },
  ];

  const emotionTrend = [
    { day: 'Lun', focus: 65, stress: 30 },
    { day: 'Mar', focus: 72, stress: 25 },
    { day: 'Mer', focus: 78, stress: 20 },
    { day: 'Jeu', focus: 82, stress: 15 },
    { day: 'Ven', focus: 88, stress: 18 },
    { day: 'Sam', focus: 85, stress: 22 },
    { day: 'Dim', focus: 90, stress: 10 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              {isAuthenticated ? `Bienvenue, ${user?.first_name}! 👋` : 'Bienvenue sur notre plateforme d\'apprentissage ! 👋'}
            </h1>
            <button className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition">
              Démarrer une session
            </button>
          </div>
        </div>
      </header>

      {/* Contenu principal */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Statistiques principales */}
        {stats ? (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            {[
              { label: 'Cours complétés', value: stats.courses_completed, icon: '📚' },
              { label: 'Séries actuelles', value: `${stats.current_streak}j`, icon: '🔥' },
              { label: 'Heures d\'étude', value: stats.total_hours, icon: '⏱️' },
              { label: 'Score moyen', value: `${stats.average_score}%`, icon: '⭐' },
            ].map((stat) => (
              <div
                key={stat.label}
                className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm font-medium">{stat.label}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">{stat.value}</p>
                  </div>
                  <span className="text-4xl">{stat.icon}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <p className="text-gray-600">Chargement des statistiques...</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Progression */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Progression (derniers 6 mois)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={progressData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#0284c7"
                  strokeWidth={2}
                  dot={{ fill: '#0284c7', r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* État émotionnel */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Tendance émotionnelle</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={emotionTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="focus" fill="#22c55e" name="Focus" />
                <Bar dataKey="stress" fill="#ef4444" name="Stress" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recommandations */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Recommandations personnalisées 🤖</h2>

          {recommendations && recommendations.length > 0 ? (
            <div className="space-y-4">
              {recommendations.slice(0, 3).map((rec) => (
                <div key={rec.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900">{rec.content_title}</h3>
                      <p className="text-gray-600 text-sm mt-1">{rec.reason_text}</p>
                      <div className="mt-3 flex items-center gap-2">
                        <span className="inline-block px-2 py-1 bg-primary-100 text-primary-800 text-xs rounded-full">
                          Confiance: {(rec.confidence_score * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <button className="ml-4 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition text-sm font-medium">
                      Voir
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-600">
              {isAuthenticated
                ? "Aucune recommandation disponible pour le moment."
                : "Connectez-vous pour voir vos recommandations personnalisées."
              }
            </p>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
