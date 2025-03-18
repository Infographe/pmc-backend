# Utiliser une image Python légère et sécurisée
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires (libgomp pour LightGBM)
RUN apt-get update && apt-get install -y \
    libgomp1 gcc gfortran && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copier uniquement les fichiers essentiels pour optimiser la mise en cache Docker
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers du projet après installation des dépendances
COPY . .

# Vérifier si les fichiers modèles sont bien présents (pour le debug)
RUN ls -la models/

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# Lancer l'application avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--timeout-keep-alive", "30"]
