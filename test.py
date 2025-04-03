# main.py

from fastapi import FastAPI
import logging
import os

# Création du dossier logs si besoin
os.makedirs("logs", exist_ok=True)

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api_logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Création de l'app FastAPI
app = FastAPI()

@app.get("/")
def root():
    logger.info("Appel à l'endpoint racine /")
    return {"message": "API OK"}
