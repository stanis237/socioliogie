# 🚀 Frontend React - LearnAI

## 📋 Vue d'ensemble

Frontend React complètement typé avec TypeScript pour la plateforme d'apprentissage personnalisée LearnAI.

### Caractéristiques
- ✅ Interface moderne et responsive avec Tailwind CSS
- ✅ Authentification JWT avec gestion des tokens
- ✅ Détection d'émotions en temps réel via webcam
- ✅ Dashboard avec graphiques et analytics
- ✅ Recommandations IA avec explications
- ✅ Gestion d'état avec React Hooks
- ✅ Requêtes HTTP avec axios et interceptors
- ✅ TypeScript strict pour la sécurité des types

## 🛠️ Installation

### Prérequis
- Node.js 18+
- npm ou yarn

### Étapes

```bash
# 1. Accéder au dossier frontend
cd learning_platform/frontend

# 2. Installer les dépendances
npm install

# 3. Copier et configurer l'env
cp .env.example .env.local

# 4. Démarrer le serveur de développement
npm start
```

## 📁 Structure du projet

```
frontend/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/          # Composants réutilisables
│   │   ├── ProtectedRoute.tsx
│   │   └── Navbar.tsx
│   ├── pages/              # Pages de l'application
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   └── EmotionDetector.tsx
│   ├── hooks/              # Custom hooks
│   │   ├── useAuth.ts
│   │   ├── useRecommendations.ts
│   │   └── useEmotionDetection.ts
│   ├── services/           # Services API
│   │   └── api.ts
│   ├── styles/             # Styles CSS
│   │   ├── global.css
│   │   └── index.css
│   ├── types/              # Types TypeScript
│   ├── App.tsx             # App principal
│   └── index.tsx           # Entry point
├── package.json
├── tsconfig.json
└── tailwind.config.js
```

## 🎯 Pages principales

### 1. **Login** (`/login`)
- Formulaire de connexion avec email/mot de passe
- Remember me functionality
- Validation en temps réel
- Lien vers inscription et réinitialisation

### 2. **Dashboard** (`/dashboard`)
- Statistiques utilisateur (cours complétés, streak, heures)
- Graphiques de progression
- Tendance émotionnelle
- Recommandations personnalisées avec explications IA
- Widget d'état émotionnel

### 3. **Emotion Detector** (`/emotions`)
- Accès à la webcam en direct
- Détection d'émotions en temps réel
- Analyse émotionnelle (stress, concentration, fatigue)
- Conseils d'adaptation basés sur l'état émotionnel
- Recommandation d'exercices adaptés

## 🔧 Configuration des variables d'environnement

```env
# API
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_API_TIMEOUT=30000

# JWT
REACT_APP_JWT_STORAGE_KEY=access_token
REACT_APP_REFRESH_TOKEN_KEY=refresh_token

# OpenAI (pour explications IA avancées)
REACT_APP_OPENAI_API_KEY=your_key_here

# Émotions
REACT_APP_EMOTION_API_URL=http://localhost:8000/api/emotions/detections/
REACT_APP_EMOTION_UPLOAD_INTERVAL=5000

# Debug
REACT_APP_DEBUG=true
REACT_APP_ENVIRONMENT=development
```

## 🪝 Custom Hooks

### `useAuth()`
Gestion complète de l'authentification

```typescript
const { 
  user,                    // Utilisateur connecté
  isAuthenticated,         // État d'authentification
  isLoading,              // Chargement
  error,                  // Messages d'erreur
  login,                  // Fonction de connexion
  signup,                 // Fonction d'inscription
  logout,                 // Fonction de déconnexion
  updateProfile,          // Mise à jour du profil
  resetPassword           // Réinitialisation mot de passe
} = useAuth();
```

### `useRecommendations()`
Gestion des recommandations IA

```typescript
const {
  recommendations,                    // Recommandations de contenu
  exerciseRecommendations,           // Recommandations d'exercices
  emotionState,                       // État émotionnel actuel
  isLoading,                          // Chargement
  error,                              // Messages d'erreur
  loadRecommendations,                // Charger recommandations
  loadExerciseRecommendations,        // Charger exercices
  loadEmotionState,                   // Charger état émotionnel
  sendFeedback,                       // Envoyer feedback
  generateRecommendations             // Générer nouvelles recos
} = useRecommendations();
```

### `useEmotionDetection(enabled?)`
Détection d'émotions via webcam

```typescript
const {
  isDetecting,            // En cours de détection
  isCapturing,            // Webcam active
  hasPermission,          // Permission webcam accordée
  detectionResult,        // Résultat de la détection
  analytics,              // Analytics émotionnelles
  error,                  // Messages d'erreur
  videoRef,               // Référence vidéo
  canvasRef,              // Référence canvas
  requestCameraPermission,// Demander permission
  captureAndAnalyze,      // Capturer et analyser
  startCapturing,         // Démarrer capture
  stopCapturing,          // Arrêter capture
  stopCamera,             // Fermer webcam
  loadEmotionAnalytics    // Charger analytics
} = useEmotionDetection(true);
```

## 🔐 Authentification

### Flux JWT
1. Login → reçoit `access_token` et `refresh_token`
2. Stockage dans localStorage
3. Envoi du token dans chaque requête (header `Authorization: Bearer ...`)
4. Refresh automatique du token si expiré
5. Redirect vers `/login` si erreur 401

### Interceptors
- **Request**: Ajout du token JWT
- **Response**: Gestion des erreurs 401, refresh automatique

## 🎨 Styles et Thème

### Tailwind CSS
- Theme couleurs personnalisé (primary, success, warning, danger)
- Animations custom (fadeIn, slideUp, pulseSoft, etc.)
- Responsive design (mobile-first)
- Dark mode ready (future)

### Composants réutilisables
- Cartes (`.card`, `.card-lg`)
- Badges (`.badge-primary`, `.badge-success`, etc.)
- Barres de progression
- Skeletons loading

## 📊 Graphiques

### Bibliothèques
- `recharts` - Graphiques React responsifs
- Intégration simple : `LineChart`, `BarChart`, `PieChart`, etc.

### Exemples
```typescript
import { LineChart, Line, XAxis, YAxis } from 'recharts';

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    <XAxis dataKey="name" />
    <YAxis />
    <Line type="monotone" dataKey="value" stroke="#0284c7" />
  </LineChart>
</ResponsiveContainer>
```

## 🧪 Tests

### Exécuter les tests
```bash
npm test
```

### Tests unitaires (Vitest)
```typescript
import { describe, it, expect } from 'vitest';

describe('MyComponent', () => {
  it('should render correctly', () => {
    // ...
  });
});
```

### Tests E2E (Cypress)
```bash
npm run test:e2e
```

## 🚀 Déploiement

### Build production
```bash
npm run build
```

### Déployer sur Vercel
```bash
npm install -g vercel
vercel
```

### Déployer sur Netlify
```bash
npm run build
# Puis drag & drop le dossier build sur Netlify
```

## 📱 Progressive Web App (PWA)

Le frontend est prêt pour PWA:
- `public/manifest.json` (à créer)
- Service Worker (à configurer)
- Installation sur accueil mobile

## 🔄 Communication avec le Backend

### Base URL
```
http://localhost:8000/api
```

### Endpoints principaux utilisés

**Authentification**
- `POST /users/login/` - Connexion
- `POST /users/signup/` - Inscription
- `POST /users/logout/` - Déconnexion
- `POST /users/token/refresh/` - Refresh token
- `GET /users/profile/` - Profil utilisateur
- `PATCH /users/profile/` - Mise à jour profil

**Recommandations**
- `GET /recommendations/content-recommendations/` - Recos contenu
- `GET /recommendations/exercise-recommendations/` - Recos exercices
- `POST /recommendations/generate/` - Générer recos
- `POST /recommendations/content-recommendations/{id}/feedback/` - Feedback

**Émotions**
- `POST /emotions/detections/upload_emotion_data/` - Upload image émotion
- `GET /emotions/emotional-states/current/` - État émotionnel actuel

## 🐛 Debugging

### Logs
- Tous les appels API sont loggés (dev mode)
- Erreurs affichées via toast notifications
- Console du navigateur pour plus de détails

### Redux DevTools (futur)
- Extension pour déboguer l'état global

## 📚 Ressources

- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS](https://tailwindcss.com)
- [Recharts](https://recharts.org)
- [Axios Documentation](https://axios-http.com)

## 🤝 Contribution

Pour contribuer:
1. Créer une branche feature
2. Commiter les changements
3. Faire un pull request

## 📝 Licence

MIT License - voir LICENSE.md

---

**Développé avec ❤️ pour LearnAI**
