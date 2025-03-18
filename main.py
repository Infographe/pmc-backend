from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import dill
import numpy as np
import os
import logging

# Création de l'API
app = FastAPI()

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Définition des chemins des modèles
ml_model_path = "models/LightGBM_best_model_2.pkl"
# dl_model_path = "models/average_model.pkl"

models = {}

# Configuration CORS pour autoriser les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (à adapter en prod)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

class PredictionInput(BaseModel):
    features: List[float]  # Liste de valeurs pour éviter l'erreur
    model_type: str  # "ml" ou "dl"

# Chargement des modèles
# for model_type, path in {"ml": ml_model_path, "dl": dl_model_path}.items():
for model_type, path in {"ml": ml_model_path}.items():
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                models[model_type] = dill.load(f)
            logger.info(f"✅ Modèle {model_type.upper()} chargé avec succès depuis {path}")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle {model_type.upper()} : {str(e)}")
    else:
        logger.warning(f"⚠️ Modèle {model_type.upper()} non trouvé à {path}")

@app.post("/predict")
def predict(data: PredictionInput):
    logger.info(f"🔍 Features reçues : {data.features}")
    logger.info(f"📌 Nombre de features reçues : {len(data.features)}")
    logger.info(f"📊 Modèle sélectionné : {data.model_type}")

    # Vérification si le modèle existe
    if data.model_type not in models:
        return JSONResponse(status_code=400, content={"message": "Modèle inconnu. Choisissez 'ml' ou 'dl'."})

    # Vérification du nombre de features attendu
    expected_features = 30 if data.model_type == "ml" else 60
    if len(data.features) != expected_features:
        return JSONResponse(
            status_code=400,
            content={"message": f"Le modèle {data.model_type} attend {expected_features} features, mais {len(data.features)} ont été reçues."}
        )

    try:
        # Prédiction
        prediction = models[data.model_type].predict([data.features])[0]
        logger.info(f"🧠 Prédiction du modèle : {prediction}")
        return {"prediction": float(prediction)}

    except Exception as e:
        logger.error(f"❌ Erreur lors de la prédiction : {str(e)}")
        return JSONResponse(status_code=500, content={"message": "Erreur lors de la prédiction."})
