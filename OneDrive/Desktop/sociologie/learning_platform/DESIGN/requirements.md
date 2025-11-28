# Cahier des charges - Plateforme d'apprentissage personnalisée

Date: 2025-11-21

## 1. Contexte et objectifs
- Objectif principal: fournir une plateforme d'apprentissage personnalisée qui recommande des contenus et génère des explications compréhensibles pour les apprenants.
- Public cible: étudiants, enseignants et apprenants autodidactes utilisant le parcours adaptatif.

## 2. Périmètre fonctionnel prioritaire (MVP)
- Authentification: création de compte, login, gestion du profil (learning_style, preferences).
- Gestion de contenu: catalogage des cours/exercices, métadonnées (niveau, durée, objectifs).
- Recommandations: moteur hybride (collaboratif + contenu + performance) fournissant une liste de contenus personnalisés.
- Explicabilité IA: génération d'explications en langage naturel (FR) pour chaque recommandation via OpenAI (ou fallback local).
- Emotion detection (optionnel dans MVP): capture d'état émotionnel et adaptation des recommandations.
- API RESTful pour le frontend (JSON), pagination, filtres et permissions.

## 3. Cas d'usage (user stories)
- En tant qu'apprenant, je veux voir des recommandations pertinentes classées par priorité afin de choisir ma prochaine activité.
- En tant qu'apprenant, je veux une explication claire du pourquoi d'une recommandation pour comprendre son utilité.
- En tant qu'enseignant, je veux voir des métriques de performance agrégées pour mes apprenants.
- En tant qu'administrateur, je veux contrôler la configuration des modèles IA et les clés API.

## 4. Exigences fonctionnelles détaillées
- Endpoint `GET /api/recommendations/` : renvoie recommandations + `explanation` (texte). Autorisé pour l'utilisateur authentifié.
- Endpoint `POST /api/recommendations/generate/` : déclenche génération asynchrone (Celery) et renvoie task id.
- Stocker en base: `ContentRecommendation` + `AIExplainability` lié.
- L'appel au service OpenAI doit être encapsulé dans un wrapper et instrumenté (logs, métriques).

## 5. Exigences non-fonctionnelles
- Performance: la génération d'explications doit être mise en cache (Redis) pour limiter les coûts et latence.
- Disponibilité: architecture Docker + worker Celery; tolérance aux erreurs d'API externe (fallback immédiat).
- Sécurité: ne jamais envoyer de données sensibles à OpenAI; anonymiser/minimiser le contexte.
- Scalabilité: services découplés (web / worker / cache / db) et CI automatisé.

## 6. Contraintes et dépendances
- Dépendances clefs: Django, DRF, Celery, Redis, OpenAI Python SDK.
- Base de données: MySQL (production) — utiliser SQLite pour tests locaux si besoin.
- Environnement Windows pour développement local (PowerShell); CI Ubuntu.

## 7. Privacy & conformité
- Les prompts sont conçus pour ne pas inclure d'identifiants personnels (email, nom) ni de données pouvant identifier des individus.
- Les explications sont stockées avec métadonnées minimales (source, confiance, ttl si cache).

## 8. Metrics de succès (KPIs)
- Taux de clic sur recommandation (CTR) > 15%.
- Temps moyen pour que l'API renvoie une explication (cache hit) < 200ms.
- Taux d'échecs du service OpenAI < 1% (avec fallback automatique).

## 9. Critères d'acceptation
- Les endpoints REST fonctionnent et sont couverts par tests unitaires et d'intégration.
- Les explications sont générées et visibles dans l'API; si OpenAI indisponible, le champ `reason_text` existant est utilisé.
- CI exécute tests et linter sur PRs.

## 10. Livrables immédiats
- `DESIGN/requirements.md` (ce document)
- `DESIGN/data_model.md` (schéma ER et mapping Django) — à produire
- `DESIGN/api_spec.md` (contrats d'API) — à produire

## 11. Prochaines étapes
1. Valider ce cahier des charges avec les parties prenantes.
2. Produire le modèle de données (`DESIGN/data_model.md`) et proposer modifications ciblées aux `apps/*/models.py`.
3. Spécifier l'API (`DESIGN/api_spec.md`) et ajouter les tests correspondants.

---
Si vous souhaitez que je commence directement par le modèle de données, dites "commencer modèle" ou donnez des priorités spécifiques (utilisateurs, recommandations, explicabilité).
