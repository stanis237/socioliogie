import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-toastify';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isLoading, error } = useAuth();
  const [email, setEmail] = useState(localStorage.getItem('remember_email') || '');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(!!localStorage.getItem('remember_email'));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const success = await login({ email, password, remember_me: rememberMe });

    if (!success) {
      toast.error(error || 'Erreur de connexion');
    }
  };

  const from = location.state?.from?.pathname || '/dashboard';

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center px-4">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">LearnAI</h1>
          <p className="text-primary-100">Plateforme d'apprentissage personnalisée</p>
        </div>

        {/* Formulaire */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Connexion</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email */}
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

            {/* Mot de passe */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Mot de passe
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                placeholder="Votre mot de passe"
                disabled={isLoading}
              />
            </div>

            {/* Remember me */}
            <div className="flex items-center">
              <input
                id="remember"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 text-primary-600 rounded focus:ring-primary-500"
                disabled={isLoading}
              />
              <label htmlFor="remember" className="ml-2 text-sm text-gray-700">
                Se souvenir de moi
              </label>
            </div>

            {/* Bouton soumettre */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-primary-600 text-white py-2 rounded-lg font-medium hover:bg-primary-700 disabled:bg-gray-400 transition"
            >
              {isLoading ? 'Connexion...' : 'Se connecter'}
            </button>
          </form>

          {/* Liens */}
          <div className="mt-6 space-y-2 text-center text-sm">
            <p className="text-gray-600">
              Pas de compte?{' '}
              <button
                type="button"
                onClick={() => navigate('/signup')}
                className="text-primary-600 font-medium hover:underline"
              >
                S'inscrire
              </button>
            </p>
            <button
              type="button"
              onClick={() => navigate('/forgot-password')}
              className="text-gray-500 hover:text-primary-600 transition"
            >
              Mot de passe oublié?
            </button>
          </div>
        </div>

        {/* Footer */}
        <p className="text-center text-primary-100 mt-8 text-sm">
          © 2024 LearnAI. Tous droits réservés.
        </p>
      </div>
    </div>
  );
};

export default Login;
