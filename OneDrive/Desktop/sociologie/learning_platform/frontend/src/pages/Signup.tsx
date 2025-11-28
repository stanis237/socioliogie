import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { toast } from 'react-toastify';

const Signup: React.FC = () => {
  const navigate = useNavigate();
  const { signup, isLoading, error } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: ''
  });
  const [rememberMe, setRememberMe] = useState(!!localStorage.getItem('remember_email'));

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (formData.password !== formData.password_confirm) {
      toast.error('Les mots de passe ne correspondent pas');
      return;
    }

    const success = await signup({ ...formData, remember_me: rememberMe });

    if (success) {
      toast.success('Inscription réussie !');
      // Navigation handled by useAuth hook
    } else {
      toast.error(error || 'Erreur lors de l\'inscription');
    }
  };

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
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Inscription</h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Prénom */}
            <div>
              <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
                Prénom
              </label>
              <input
                id="first_name"
                name="first_name"
                type="text"
                required
                value={formData.first_name}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                placeholder="Votre prénom"
                disabled={isLoading}
              />
            </div>

            {/* Nom */}
            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
                Nom
              </label>
              <input
                id="last_name"
                name="last_name"
                type="text"
                required
                value={formData.last_name}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                placeholder="Votre nom"
                disabled={isLoading}
              />
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
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
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                placeholder="Votre mot de passe"
                disabled={isLoading}
              />
            </div>

            {/* Confirmation mot de passe */}
            <div>
              <label htmlFor="password_confirm" className="block text-sm font-medium text-gray-700 mb-1">
                Confirmer le mot de passe
              </label>
              <input
                id="password_confirm"
                name="password_confirm"
                type="password"
                required
                value={formData.password_confirm}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                placeholder="Confirmer votre mot de passe"
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
              {isLoading ? 'Inscription...' : 'S\'inscrire'}
            </button>
          </form>

          {/* Liens */}
          <div className="mt-6 text-center text-sm">
            <p className="text-gray-600">
              Déjà un compte?{' '}
              <button
                type="button"
                onClick={() => navigate('/login')}
                className="text-primary-600 font-medium hover:underline"
              >
                Se connecter
              </button>
            </p>
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

export default Signup;
