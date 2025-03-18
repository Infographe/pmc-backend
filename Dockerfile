# Utiliser une image Python légère et sécurisée
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libgomp1 gcc gfortran && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier uniquement les fichiers nécessaires pour éviter d'invalider le cache Docker
COPY requirements.txt .

# Installer les dépendances Python avec `--no-cache-dir` pour réduire la taille de l'image
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers après l'installation des dépendances (optimisation du cache)
COPY . .

# Supprimer les fichiers inutiles pour alléger l'image
RUN find . -name "*.pyc" -o -name "*.pyo" -o -name "__pycache__" | xargs rm -rf

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Lancer l'application avec Uvicorn en mode production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--timeout-keep-alive", "30"]
