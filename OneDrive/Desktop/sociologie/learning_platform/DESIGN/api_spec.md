# Spécification API - Plateforme d'apprentissage

Version: 1.0

Base URL: `/api/`

Authentification: JWT (Simple JWT) — les endpoints protégés exigent l'en-tête `Authorization: Bearer <token>`.

Conventions:
- Responses: JSON
- Pagination: `limit` / `offset` query params (ou DRF pagination)
- Erreurs: format `{ "detail": "message" }`

## Endpoints principaux

### Auth
- `POST /api/auth/register/` : créer un compte
  - Body: `{ "email": "...", "password": "...", "first_name": "", "last_name": "" }`
  - Response: `201` avec user summary (id, email)

- `POST /api/auth/token/` : obtenir JWT
  - Body: `{ "email": "...", "password": "..." }`
  - Response: `{ "access": "...", "refresh": "..." }`

### Content
- `GET /api/courses/` : lister cours
  - Query: `?category=&level=&status=published&limit=&offset=`
  - Response: list of courses with fields: `id, title, description, category, level, duration_minutes, status`

- `GET /api/courses/{id}/` : détail d'un cours

### Recommendations
- `GET /api/recommendations/` : récupérer recommandations pour l'utilisateur courant
  - Required: Auth
  - Query: `?limit=10`
  - Response item: {
    `id`, `recommended_course`: {`id`,`title`}, `reason`, `reason_explanation`, `confidence_score`, `priority`, `created_at`, `explanation` (alias for `reason_explanation`)
  }

- `POST /api/recommendations/generate/` : déclenche génération asynchrone
  - Body (optional): `{ "limit": 5 }`
  - Response: `202` `{ "task_id": "..." }`
  - Implementation note: déclenche Celery task qui appelle RecommendationService.generate_recommendations puis save_recommendations

- `GET /api/recommendations/{id}/` : détail d'une recommandation et `explanation` complet

### AI Explainability
- `GET /api/recommendations/{id}/explanation/` : renvoie l'objet `AIExplainability` lié si existant
  - Response: `{ "user_friendly_explanation": "...", "factors": [...], "supporting_data": {...}, "source": "ai" }`

### Emotions (optionnel)
- `POST /api/emotions/detect/` : poster une détection émotionnelle (utilisé par frontend)
  - Body: `{ "detected_emotion": "happy", "confidence": 0.92, "metadata": {...} }`
  - Response: `201` avec created detection

### Admin / Monitoring
- `GET /api/admin/openai/status/` : renvoie état des quotas et dernières erreurs (admin only)

## Schémas (exemples)
- Recommendation response example:

```
{
  "id": 123,
  "recommended_course": {"id": 54, "title": "Intro à la sociologie"},
  "reason": "performance",
  "reason_explanation": "Parce que vos résultats récents montrent un besoin de renforcement sur ce sujet.",
  "confidence_score": 0.88,
  "priority": 1,
  "created_at": "2025-11-20T12:34:56Z"
}
```

## Sécurité et quotas
- Les endpoints d'IA ne doivent jamais logguer intégralement le prompt contenant des données utilisateur.
- Ajouter rate limiting sur endpoints sensibles (ex: generate explanations) pour protéger la facturation OpenAI.

## Tests à prévoir
- Tests unitaires pour chaque endpoint: permissions, schémas, erreurs.
- Tests d'intégration pour la chaîne: déclenchement de la tâche → enregistrement `ContentRecommendation` + `AIExplainability`.
