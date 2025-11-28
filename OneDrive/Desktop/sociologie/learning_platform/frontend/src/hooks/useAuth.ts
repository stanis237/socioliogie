import { useState, useCallback, useEffect } from 'react';
import api from '../services/api';
import { useNavigate } from 'react-router-dom';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  profile_picture?: string;
  learning_style?: string;
  created_at: string;
}

interface AuthResponse {
  access: string;
  refresh: string;
  user: User;
}

interface LoginCredentials {
  email: string;
  password: string;
  remember_me?: boolean;
}

interface SignupData extends LoginCredentials {
  first_name: string;
  last_name: string;
  password_confirm: string;
  remember_me?: boolean;
}

export const useAuth = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Vérifier l'état d'authentification au chargement
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = api.getAccessToken();
        if (token && api.isTokenValid(token)) {
          // Récupérer les infos utilisateur
          const userData = await api.get<User>('/users/profile/');
          setUser(userData);
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (err) {
        setIsAuthenticated(false);
        api.clearTokens();
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(
    async (credentials: LoginCredentials): Promise<boolean> => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await api.post<AuthResponse>('/users/login/', {
          email: credentials.email,
          password: credentials.password,
        });

        api.setTokens(response.access, response.refresh);
        setUser(response.user);
        setIsAuthenticated(true);

        if (credentials.remember_me) {
          localStorage.setItem('remember_email', credentials.email);
        }

        navigate('/dashboard');
        return true;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.message ||
          'Erreur de connexion. Vérifiez vos identifiants.';
        setError(errorMessage);
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    [navigate]
  );

  const signup = useCallback(
    async (data: SignupData): Promise<boolean> => {
      setIsLoading(true);
      setError(null);

      try {
        if (data.password !== data.password_confirm) {
          throw new Error('Les mots de passe ne correspondent pas');
        }

        const response = await api.post<AuthResponse>('/users/signup/', {
          email: data.email,
          password: data.password,
          password_confirm: data.password_confirm,
          first_name: data.first_name,
          last_name: data.last_name,
        });

        api.setTokens(response.access, response.refresh);
        setUser(response.user);
        setIsAuthenticated(true);

        navigate('/dashboard');
        return true;
      } catch (err: any) {
        const errorMessage =
          err.response?.data?.message ||
          'Erreur lors de la création du compte';
        setError(errorMessage);
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    [navigate]
  );

  const logout = useCallback(async () => {
    setIsLoading(true);

    try {
      await api.post('/users/logout/', {});
    } catch (err) {
      console.error('Erreur lors de la déconnexion:', err);
    } finally {
      api.clearTokens();
      setUser(null);
      setIsAuthenticated(false);
      setIsLoading(false);
      navigate('/login');
    }
  }, [navigate]);

  const updateProfile = useCallback(async (updates: Partial<User>) => {
    setIsLoading(true);
    setError(null);

    try {
      const updated = await api.patch<User>('/users/profile/', updates);
      setUser(updated);
      return true;
    } catch (err: any) {
      setError('Erreur lors de la mise à jour du profil');
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const resetPassword = useCallback(async (email: string) => {
    setIsLoading(true);
    setError(null);

    try {
      await api.post('/users/password-reset/', { email });
      return true;
    } catch (err: any) {
      setError('Erreur lors de la demande de réinitialisation');
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    signup,
    logout,
    updateProfile,
    resetPassword,
  };
};
