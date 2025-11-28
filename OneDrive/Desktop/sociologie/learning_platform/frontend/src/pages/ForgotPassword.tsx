import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-toastify';

const ForgotPassword: React.FC = () => {
  const navigate = useNavigate();
  const { resetPassword, isLoading, error } = useAuth();
  const [email, setEmail] = useState('');
  const [emailSent, setEmailSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const success = await resetPassword(email);

    if (success) {
      setEmailSent(true);
      toast.success('Email de réinitialisation envoyé !');
    } else {
      toast.error(error || 'Erreur lors de l\'envoi de l\'email');
    }
  };

  if (emailSent) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center px-4">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">LearnAI</h1>
            <p className="text-primary-100">Plateforme d'apprentissage personnalisée</p>
          </div>

          <div className="bg-white rounded-lg shadow-xl p-8 text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Email envoyé !</h2>
            <p className="text-gray-600 mb-6">
              Nous avons envoyé un lien de réinitialisation à <strong>{email}</strong>.
            </p>
            <button
              onClick={() => navigate('/login')}
              className="w-full bg-primary-600 text-white py-2 rounded-lg font-medium hover:bg-primary-700 transition"
            >
              Retour à la connexion
            </button>
          </div>

          <p className="text-center text-primary-100 mt-8 text-sm">
            © 2025 LearnAIdevstanis. Tous droits réservés.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">LearnAI</h1>
          <p className="text-primary-100">Plateforme d'apprentissage personnalisée</p>
        </div>

        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Mot de passe oublié</h2>
          <p className="text-gray-600 mb-6">
            Entrez votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe.
          </p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                placeholder="votre.email@example.com"
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary-600 text-white py-2 rounded-lg font-medium hover:bg-primary-700 disabled:bg-gray-400 transition"
            >
              {isLoading ? 'Envoi en cours...' : 'Envoyer le lien'}
            </button>
          </form>

          <div className="mt-6 text-center text-sm">
            <button
              type="button"
              onClick={() => navigate('/login')}
              className="text-primary-600 font-medium hover:underline"
            >
              Retour à la connexion
            </button>
          </div>
        </div>

        <p className="text-center text-primary-100 mt-8 text-sm">
          © 2025 LearnAI DEVSTANIS. Tous droits réservés.
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;
