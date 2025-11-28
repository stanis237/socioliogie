# Sécurité & Gestion des secrets

## Principes généraux
- Ne pas committer de secrets (clé OpenAI, mots de passe DB). Utiliser `.env` localement et `GitHub Secrets`/Vault en prod.
- Principe du moindre privilège pour comptes de services.

## Gestion des clés OpenAI
- Stocker `OPENAI_API_KEY` dans les secrets du dépôt ou un secret manager.
- Procédure de rotation: documenter étapes pour révoquer et remplacer une clé (Quickstart + README ops).

## Authentification & autorisation
- Utiliser JWT (Simple JWT) avec refresh tokens; stocker tokens côté client de façon sécurisée (httpOnly cookies recommandés).

## Protection API
- Rate limiting sur endpoints coûteux (OpenAI, génération) par IP et par utilisateur.
- Validation stricte des inputs, sanitation, length limits.

## Données sensibles & RGPD
- Minimiser les données envoyées aux services tiers.
- Fournir mécanisme pour suppression des données utilisateur (Droit à l'oubli).

## Logging
- Ne pas stocker prompts ou données identifiantes dans logs; stocker des hashes/IDs si besoin.
