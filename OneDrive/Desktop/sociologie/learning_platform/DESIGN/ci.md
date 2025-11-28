# CI / CD et qualité

Objectif: définir les workflows CI (tests, linter, type checks) et bonnes pratiques pour PRs.

## Workflow recommandé (GitHub Actions)
- Triggers: `push` (branches main/master), `pull_request`.
- Jobs:
  - `lint`: exécute `ruff` / `flake8` et `isort` (optionnel)
  - `type-check`: exécute `mypy` si configuré
  - `tests`: installe dépendances et lance `pytest` (utiliser matrix python versions si besoin)
  - `build`: build et push docker image (sur `main`)

## Secrets & variables
- `OPENAI_API_KEY` doit être stocké en `Secrets` et injecté uniquement pour les jobs nécessaires.

## Example: checks rapides
- `lint` (fail fast)
- `tests` (run with `-k "not slow"` for PR quick checks; full test suite on scheduled runs)

## Artifacts
- Conserver rapports de couverture, logs pytest, et rapports de linter comme artifacts CI.

## Notifications
- Intégrer badge de statut dans le README.
