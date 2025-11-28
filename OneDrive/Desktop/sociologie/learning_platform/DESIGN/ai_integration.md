# Intégration IA - OpenAI et explicabilité

Objectif: définir la manière dont la plateforme utilise OpenAI pour générer des explications utilisateur, en respectant la vie privée, la résilience et l'efficience coût/latence.

## Architecture
- Wrapper centralisé: `ai_module/openai_service.py` expose `generate_explanation(payload, user_context=None)`.
- Service d'appel: `ai_module/services.RecommendationService.save_recommendations` utilise le wrapper pour obtenir `user_friendly_explanation` puis crée `AIExplainability`.

## Prompt design (principes)
- Langue: français par défaut.
- Longueur: court et concret (1-3 phrases), pas d'informations personnelles.
- Format de sortie: texte brut, 1-3 phrases, ton pédagogique.

Prompt example (safeguarded):

"Vous êtes un tuteur pédagogique concis. Expliquez en 1-2 phrases pourquoi le cours \"{title}\" est recommandé pour un apprenant qui présente {reason} (score: {score}). Ne mentionnez aucune donnée personnelle." 

## Données envoyées
- Autoriser uniquement: `title`, `reason`, `score`, `factors` (agrégés, anonymisés), `learning_style` (non-identifiant), `recent_average` (valeur numérique agrégée).
- Ne pas envoyer: email, nom, identifiants, notes brutes, données sensibles.

## Caching
- Utiliser `django.core.cache` (backend Redis). Key: hash(user_id, course_id, reason, score_rounded)
- Configs: `OPENAI_CACHE_ENABLED` (bool), `OPENAI_EXPLANATION_TTL` (seconds). Defaults: enabled=True, ttl=86400.
- Flow: if cache hit → return cached explanation; else call OpenAI → store with TTL → return.

## Fallbacks & résilience
- Si OpenAI indisponible ou l'appel échoue: utiliser `reason_text` fourni par le moteur interne.
- Loggez les erreurs et incrémentez un compteur métrique (ex: sentry / prometheus). Ne logguez pas le prompt complet.
- Politique de retry: 1 retry avec backoff court pour erreurs transitoires (5xx, timeout).

## Sécurité & coût
- Ajouter rate-limit par utilisateur sur les appels OpenAI (ex: 10 appels / heure).
- Configurer quota d'alerte pour dépenses OpenAI.
- Stocker la clé OpenAI dans `OPENAI_API_KEY` (env / GitHub Secret) — ne pas committer.

## Monitoring & métriques
- Exposer métriques: cache_hit_rate, openai_call_count, openai_errors, latency_ms.
- Ajouter logs structurés pour erreurs et durées (ne pas inclure prompt textuel complet).

## Tests
- Unit tests: mock `openai_service.generate_explanation` to validate flows (success, None, exception).
- Cache tests: mock cache get/set to ensure behavior.
- Integration: end-to-end test that simulates recommendation generation and ensures `AIExplainability` persisted.
