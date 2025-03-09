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

# 🔹 Configuration CORS pour autoriser les requêtes du frontend
origins = [
    "https://pmc-frontend-gvo6.onrender.com",  # ✅ URL de ton frontend sur Render
    "http://localhost:4200",  # ✅ Pour développement local
    "http://127.0.0.1:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ Liste des origines autorisées
    allow_credentials=True,
    allow_methods=["*"],  # ✅ Autoriser toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # ✅ Autoriser tous les headers
)

# Définition des entrées pour la prédiction
# Définition des entrées pour la prédiction (30 features)
class PredictionInput(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    feature4: float
    feature5: float
    feature6: float
    feature7: float
    feature8: float
    feature9: float
    feature10: float
    feature11: float
    feature12: float
    feature13: float
    feature14: float
    feature15: float
    feature16: float
    feature17: float
    feature18: float
    feature19: float
    feature20: float
    feature21: float
    feature22: float
    feature23: float
    feature24: float
    feature25: float
    feature26: float
    feature27: float
    feature28: float
    feature29: float
    feature30: float


@app.post("/predict")
def predict(data: PredictionInput):
    """
    Prend une requête avec 30 features et retourne une prédiction.
    """
    try:
        # Extraction des valeurs sous forme de liste
        features = np.array([[getattr(data, f"feature{i}") for i in range(1, 31)]])

        # Prédiction
        prediction = model.predict(features)[0]

        logger.info(f"🔍 Prédiction effectuée : {prediction}")
        return {"prediction": float(prediction)}

    except Exception as e:
        logger.error(f"❌ Erreur lors de la prédiction : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur lors de la prédiction.")
