# Utilisation d’une image Python légère
FROM python:3.9-slim

WORKDIR /app

# Installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Commande pour exécuter l'API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
