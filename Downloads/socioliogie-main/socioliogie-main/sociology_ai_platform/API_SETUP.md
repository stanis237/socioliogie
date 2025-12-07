# Configuration des API pour le générateur de cours

Ce document explique comment configurer les clés API nécessaires pour utiliser le générateur de cours avec YouTube, Google Search et ChatGPT.

## Services utilisés

1. **YouTube** : Pour rechercher des vidéos éducatives pertinentes
2. **Google Search API** : Pour trouver de la documentation en ligne
3. **OpenAI (ChatGPT)** : Pour générer des quiz et exercices adaptés

## Configuration

### 1. Variables d'environnement

Ajoutez les clés API suivantes dans vos variables d'environnement ou dans le fichier `.env` :

```bash
# YouTube API (optionnel - utilise youtube-search-python qui ne nécessite pas de clé)
# YOUTUBE_API_KEY=votre_cle_youtube

# Google Search API (SerpAPI)
GOOGLE_SEARCH_API_KEY=votre_cle_serpapi
GOOGLE_SEARCH_ENGINE_ID=votre_engine_id

# OpenAI API
OPENAI_API_KEY=votre_cle_openai
```

### 2. Obtenir les clés API

#### YouTube (Optionnel)
- Le système utilise `youtube-search-python` qui ne nécessite pas de clé API
- Si vous souhaitez utiliser l'API officielle YouTube, obtenez une clé sur [Google Cloud Console](https://console.cloud.google.com/)

#### Google Search API (SerpAPI)
1. Créez un compte sur [SerpAPI](https://serpapi.com/)
2. Obtenez votre clé API depuis le dashboard
3. Créez un moteur de recherche personnalisé sur [Google Custom Search](https://programmablesearchengine.google.com/)
4. Récupérez l'Engine ID de votre moteur de recherche

#### OpenAI API
1. Créez un compte sur [OpenAI](https://platform.openai.com/)
2. Allez dans la section API Keys
3. Créez une nouvelle clé API
4. Copiez la clé (elle ne sera affichée qu'une seule fois)

### 3. Configuration dans Django

Les clés sont automatiquement chargées depuis les variables d'environnement dans `settings.py` :

```python
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
GOOGLE_SEARCH_API_KEY = os.environ.get('GOOGLE_SEARCH_API_KEY', '')
GOOGLE_SEARCH_ENGINE_ID = os.environ.get('GOOGLE_SEARCH_ENGINE_ID', '')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
```

### 4. Installation des dépendances

Installez les packages nécessaires :

```bash
pip install -r requirements.txt
```

Les packages suivants seront installés :
- `youtube-search-python` : Pour rechercher des vidéos YouTube
- `google-search-results` : Pour utiliser SerpAPI (Google Search)
- `openai` : Pour utiliser l'API ChatGPT

## Fonctionnement

### Génération de cours

Le générateur de cours utilise maintenant :

1. **Vidéos YouTube** : Recherche automatique de vidéos pertinentes selon le sujet et le niveau
2. **Documentation Google** : Recherche de ressources documentaires en ligne
3. **Quiz ChatGPT** : Génération de quiz adaptés au niveau de l'étudiant
4. **Exercices ChatGPT** : Création d'exercices personnalisés selon le niveau

### Adaptation au profil étudiant

Le système adapte automatiquement :
- La difficulté des quiz et exercices selon le niveau de l'étudiant
- Le contenu selon le profil utilisateur (débutant, intermédiaire, avancé)
- Les recommandations selon l'émotion détectée

## Notes importantes

- **YouTube** : Fonctionne sans clé API grâce à `youtube-search-python`
- **Google Search** : Nécessite un compte SerpAPI (service payant avec plan gratuit limité)
- **ChatGPT** : Nécessite un compte OpenAI avec crédits (payant)

Si une API n'est pas configurée, le système utilisera des fallbacks (contenu générique) pour continuer à fonctionner.

## Dépannage

### Erreur "Module not found"
```bash
pip install youtube-search-python google-search-results openai
```

### Erreur "API key not found"
Vérifiez que vos variables d'environnement sont bien définies :
```bash
echo $OPENAI_API_KEY
echo $GOOGLE_SEARCH_API_KEY
```

### Erreur de quota API
- Vérifiez vos limites d'utilisation sur les dashboards respectifs
- Les services gratuits ont des limites (SerpAPI : 100 recherches/mois, OpenAI : selon votre plan)

