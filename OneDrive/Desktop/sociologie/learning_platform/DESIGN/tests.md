# Stratégie de tests

But: définir une stratégie claire pour couvrir le code (unit, integration, e2e) et les étapes à automatiser en CI.

## Niveaux de tests
- Unit tests: logique métier (recommendation engine, ai wrapper mocks, serializers).
- Integration tests: endpoints + DB interactions (use test DB SQLite or ephemeral MySQL container).
- End-to-end: scénario utilisateur complet (login → generate recommendations → view explanation), idéalement via Playwright / Cypress pour le frontend.

## Fixtures et données
- fournir des fixtures pour utilisateurs types (novice, avancé), contenus et metrics.
- factories: utiliser `factory_boy` pour créer objets test rapidement.

## Tests pour l'intégration OpenAI
- Mock `ai_module.openai_service.generate_explanation` to avoid external calls.
- Tests for caching behavior (cache hit/miss), fallback on exception, and correct persistence of `AIExplainability`.

## CI execution
- Quick checks on PRs: `lint` + `pytest -q -k "not slow"`.
- Full test suite on merge to main or scheduled nightly build.

## Coverage & Quality
- Collect coverage (coverage.py) and fail build if coverage < threshold (e.g., 80%).
