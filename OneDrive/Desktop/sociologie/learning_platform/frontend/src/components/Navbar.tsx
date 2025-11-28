import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link to="/dashboard" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-primary-600">LearnAI</span>
            <span className="text-gray-500">|</span>
            <span className="text-sm text-gray-600">Apprentissage Personnalisé</span>
          </Link>

          {/* Menu desktop */}
          <div className="hidden md:flex items-center space-x-8">
            <Link
              to="/dashboard"
              className="text-gray-700 hover:text-primary-600 font-medium transition"
            >
              Dashboard
            </Link>
            <Link
              to="/emotions"
              className="text-gray-700 hover:text-primary-600 font-medium transition"
            >
              Émotions
            </Link>
            <a
              href="#"
              className="text-gray-700 hover:text-primary-600 font-medium transition"
            >
              Cours
            </a>
            <a
              href="#"
              className="text-gray-700 hover:text-primary-600 font-medium transition"
            >
              Exercices
            </a>
          </div>

          {/* Profil et actions */}
          <div className="flex items-center space-x-4">
            {/* User menu */}
            <div className="relative group">
              <button className="flex items-center space-x-2 px-4 py-2 rounded-lg hover:bg-gray-100 transition">
                <div className="w-8 h-8 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-bold">
                    {user?.first_name.charAt(0).toUpperCase()}
                  </span>
                </div>
                <span className="text-sm font-medium text-gray-700 hidden sm:inline">
                  {user?.first_name}
                </span>
              </button>

              {/* Dropdown */}
              <div className="absolute right-0 mt-0 w-48 bg-white rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition duration-200">
                <Link
                  to="#"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 border-b"
                >
                  Mon profil
                </Link>
                <Link
                  to="#"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 border-b"
                >
                  Paramètres
                </Link>
                <Link
                  to="#"
                  className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 border-b"
                >
                  Aide
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                >
                  Déconnexion
                </button>
              </div>
            </div>

            {/* Menu mobile */}
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>

        {/* Menu mobile */}
        {isOpen && (
          <div className="md:hidden py-4 space-y-2 border-t">
            <Link
              to="/dashboard"
              className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Dashboard
            </Link>
            <Link
              to="/emotions"
              className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Émotions
            </Link>
            <a
              href="#"
              className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Cours
            </a>
            <a
              href="#"
              className="block px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg"
            >
              Exercices
            </a>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
