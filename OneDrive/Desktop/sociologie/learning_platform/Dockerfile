FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    mysql-client \
    libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le projet
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p /app/logs /app/staticfiles /app/media

# Exposer le port
EXPOSE 8000

# Commande par défaut
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
