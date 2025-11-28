# Quickstart

1) Installer les dépendances Python (venv recommandé)

```powershell
cd c:\Users\Lenovo\OneDrive\Desktop\sociologie\learning_platform
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Configurer les variables d'environnement

- Copier le modèle `.env.example` et renseigner vos valeurs (NE PAS committer la vraie clé)

```powershell
copy .env.example .env
# Éditez .env et ajoutez votre clé OPENAI_API_KEY
```

Pour définir la clé OpenAI en PowerShell (temporaire pour la session) :

```powershell
$env:OPENAI_API_KEY = "sk-..."
$env:OPENAI_MODEL = "gpt-4o-mini"  # optionnel
```

Important: si vous avez publié votre clé par erreur (par ex. dans un chat), **révoquez-la immédiatement** depuis le tableau de bord OpenAI et générez-en une nouvelle.

3) Appliquer les migrations et lancer le serveur

```powershell
python manage.py migrate
python manage.py runserver
```

4) Frontend (optionnel)

```powershell
cd frontend
npm install
npm start
```

Sécurité & bonnes pratiques
- Ne **jamais** committer des secrets (API keys) dans le dépôt.
- Utilisez un gestionnaire de secrets (Vault, Azure Key Vault, AWS Secrets Manager) pour la production.
- En développement, stockez la clé dans `.env` et ajoutez `.env` à `.gitignore`.
