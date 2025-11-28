# Déploiement et infrastructure

But: définir l'architecture production et les services nécessaires pour exécuter la plateforme (web, worker, cache, DB, stockage médias).

## Topologie (Docker Compose)
- `web`: Django app (Gunicorn + Daphne si websockets), expose port 8000
- `worker`: Celery worker (référence: `celery -A config worker -l info`)
- `beat`: (optionnel) Celery beat pour tâches planifiées
- `redis`: cache & broker
- `db`: MySQL / MariaDB (ou RDS)
- `nginx`: reverse proxy, gestion SSL
- `storage`: volumes pour médias statiques ou objet (S3 en prod)

Exemple `docker-compose.yml` services (résumé):

```
services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    env_file: .env
    depends_on: [db, redis]

  worker:
    build: .
    command: celery -A config worker -l info
    env_file: .env
    depends_on: [redis, db]

  redis:
    image: redis:7

  db:
    image: mysql:8
    environment: MYSQL_ROOT_PASSWORD, MYSQL_DATABASE
```

## Configuration
- Variables d'env: `DJANGO_SECRET_KEY`, `DATABASE_URL` (or MYSQL_* vars), `REDIS_URL`, `OPENAI_API_KEY`, `DJANGO_ALLOWED_HOSTS`.
- Sécurité: utiliser `DOCKER_SECRET` / Vault pour clés sensibles en production.

## Stockage statique & média
- En local: volumes Docker. En production: S3-compatible object storage + CDN.

## Monitoring & observabilité
- Logs: centraliser (ELK / Loki)
- Metrics: Prometheus exporter + Grafana dashboards (OpenAI call latency, cache hitrate, Celery queue depth)

## Scalabilité
- Web: scale via replicas behind load-balancer
- Worker: scale Celery workers based on queue depth

## CI/CD
- Image build → tests → push image to registry → deploy (via GitHub Actions / GitLab CI / ArgoCD)
