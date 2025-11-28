#!/bin/bash

# Script d'installation automatique
# Usage: bash setup.sh

set -e

echo "=== Plateforme d'Apprentissage IA - Setup ==="
echo ""

# Vérifier les prérequis
echo "Vérification des prérequis..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non trouvé. Installez Python 3.9+"
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "❌ pip non trouvé"
    exit 1
fi

echo "✓ Python trouvé: $(python3 --version)"

# Créer l'environnement virtuel
echo ""
echo "Création de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Environnement virtuel créé"
else
    echo "✓ Environnement virtuel existe déjà"
fi

# Activer l'env
source venv/bin/activate || . venv/Scripts/activate

# Installer les dépendances
echo ""
echo "Installation des dépendances..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✓ Dépendances installées"

# Copier .env
echo ""
echo "Configuration de l'environnement..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Fichier .env créé (à configurer)"
else
    echo "✓ Fichier .env existe déjà"
fi

# Migrations
echo ""
echo "Initialisation de la base de données..."
python manage.py migrate
echo "✓ Migrations appliquées"

# Collecter les fichiers statiques
echo ""
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput
echo "✓ Fichiers statiques collectés"

# Créer un super-utilisateur
echo ""
echo "Création d'un super-utilisateur (admin)..."
python manage.py createsuperuser

echo ""
echo "=== Setup terminé ! ==="
echo ""
echo "Pour lancer le serveur :"
echo "  python manage.py runserver"
echo ""
echo "L'API sera disponible sur http://localhost:8000/"
echo "L'admin sur http://localhost:8000/admin/"
echo ""
