from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import dill
import pickle
import os
import logging
import traceback
import uvicorn

# 📌 Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 📌 Création de l'API
app = FastAPI()

# 📌 Configuration CORS pour autoriser les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📌 Définition des features sous forme d'objet
class FeatureInput(BaseModel):
    Cyclepds: float
    region: float
    dept: float
    annee: float
    mois: float
    pm10: float
    carbon_monoxide: float
    poids_moyen: float
    regime_special: float
    p_animal: float
    agglo9: float
    entrerep: float
    fastfood: float
    ozone: float
    dip: float
    sulphur_dioxide: float
    temps_act_phy: float
    sedentaire: float
    sexeps: float
    vistes_medecins: float
    pm2_5: float
    taille: float
    IMC: float
    situ_prof: float
    grass_pollen: float
    enrich: float
    heur_trav: float
    situ_mat: float
    nitrogen_dioxide: float
    fqvpo: float

class PredictionInput(BaseModel):
    model_type: str  # "ml" ou "dl"
    features: dict  # Attente d'un objet JSON avec des clés numériques

# 📌 Fonction pour charger les modèles
def load_model(model_path):
    try:
        if not os.path.exists(model_path):
            logger.error(f"❌ Le fichier {model_path} est introuvable.")
            return None
        
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        
        if not hasattr(model, "predict") or not callable(model.predict):
            raise ValueError(f"⚠️ Le modèle chargé depuis {model_path} ne possède pas de méthode `predict()`.")

        logger.info(f"✅ Modèle chargé avec succès : {model_path}")
        return model
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement du modèle {model_path} : {str(e)}")
        logger.error(traceback.format_exc())
        return None

# 📌 Définition des chemins des modèles
ml_model_path = "models/LightGBM_best_model_2.pkl"
dl_model_path = "models/XGBoost_best_model.pkl"

# 📌 Chargement des modèles
models = {
    "ml": load_model(ml_model_path),
    "dl": load_model(dl_model_path),
}

# 📌 Vérification du contenu du dossier models
logger.info(f"📂 Contenu du dossier models : {os.listdir('models')}")

# 📌 Routes API
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de prédiction 🎉"}

@app.get("/health")
def health():
    return {"status": "API is running 🚀"}

@app.post("/predict")
async def predict(data: dict):
    try:
        print("📡 Données reçues :", data)  # 🔍 Debugging
        if "features" not in data:
            raise HTTPException(status_code=400, detail="Les features sont manquantes.")

        # Exemple de simulation de prédiction
        prediction = np.random.rand() * 10  # Simule un modèle
        print("✅ Prédiction générée :", prediction)

        return {"prediction": round(prediction, 2)}  # ✅ Renvoie un float bien formaté

    except Exception as e:
        print("❌ Erreur lors de la prédiction :", str(e))
        return {"error": f"Erreur de prédiction : {str(e)}"}