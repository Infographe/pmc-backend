from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import dill
import numpy as np
import os
import logging
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Vérifier si le modèle existe avant de le charger
model_path = "models/average_model.pkl"

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Modèle non trouvé : {model_path}. Exécutez 'train_model.py' pour le générer.")

# Charger le modèle avec gestion des erreurs
try:
    with open(model_path, "rb") as f:
        model = dill.load(f)
    logger.info(f"✅ Modèle chargé avec succès depuis {model_path}")
except Exception as e:
    raise RuntimeError(f"Erreur lors du chargement du modèle : {str(e)}")

# Création de l'API
app = FastAPI()

# 🔹 Gestion des permissions CORS (Autoriser toutes les requêtes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition des entrées pour la prédiction
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float

@app.post("/predict")
def predict(data: PredictionInput):
    """
    Prend une requête avec 5 features et retourne une prédiction.
    """
    try:
        features = np.array([[data.feature1, data.feature2, data.feature3, data.feature4, data.feature5]])
        prediction = model.predict(features)[0]
        logger.info(f"🔍 Prédiction effectuée : {prediction}")
        return {"prediction": float(prediction)}
    except Exception as e:
        logger.error(f"❌ Erreur lors de la prédiction : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur lors de la prédiction.")
