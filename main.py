from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import dill
import os
import logging
from typing import List
import traceback  # Ajout pour afficher l'erreur complète
import os
import uvicorn


# Création de l'API
app = FastAPI()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render assigne un port automatiquement
    uvicorn.run(app, host="0.0.0.0", port=port)


# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import pickle
import os

def load_model(model_path):
    try:
        print(f"🔍 Tentative de chargement du modèle : {model_path}")
        with open(model_path, "rb") as file:
            model = pickle.load(file)
        print(f"✅ Modèle chargé avec succès : {model_path}")
        return model
    except Exception as e:
        print(f"❌ Erreur lors du chargement du modèle {model_path} : {str(e)}")
        return None  # Retourne None si le chargement échoue

# Charger les modèles
ml_model_path = "models/LightGBM_best_model_2.pkl"
dl_model_path = "models/XGBoost_best_model.pkl"

print(f"📂 Contenu du dossier models : {os.listdir('models')}")  # Vérifier si les fichiers existent bien

ml_model = load_model(ml_model_path)
dl_model = load_model(dl_model_path)

# # Définition des chemins des modèles
# ml_model_path = "models/LightGBM_best_model_2.pkl"
# dl_model_path = "models/XGBoost_best_model.pkl"

models = {}

# Configuration CORS pour autoriser les requêtes du frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition des features sous forme d'objet
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


# Chargement des modèles
for model_choice, path in {"ml": ml_model_path, "dl": dl_model_path}.items():
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                models[model_choice] = dill.load(f)
            logger.info(f"✅ Modèle {model_choice.upper()} chargé avec succès depuis {path}")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement du modèle {model_choice.upper()} : {str(e)}")
    else:
        logger.warning(f"⚠️ Modèle {model_choice.upper()} non trouvé à {path}")
        
@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API de prédiction 🎉"}

@app.get("/health")
def health():
    return {"status": "API is running 🚀"}

@app.post("/predict")
def predict(data: PredictionInput):
    # logger.info(f"📩 Données reçues par l'API : {data.dict()}")  # ✅ Debugging

    # if data.model_type not in models:
    #     return JSONResponse(status_code=400, content={"message": "Modèle inconnu. Choisissez 'ml' ou 'dl'."})

    # try:
    #     # Vérification du format des features
    #     feature_values = list(data.features.values())  # ✅ Extraire les valeurs

    #     logger.info(f"🔍 Features après conversion : {feature_values}")

    #     prediction = models[data.model_type].predict([feature_values])[0]
    #     logger.info(f"🧠 Prédiction du modèle : {prediction}")

    #     return {"prediction": float(prediction)}

    # except Exception as e:
    #     logger.error(f"❌ Erreur lors de la prédiction : {str(e)}")
    #     return JSONResponse(status_code=500, content={"message": "Erreur lors de la prédiction."})
    print("📩 Données reçues :", data)
    
    model = ml_model if data.model_type == "ml" else dl_model

    if model is None:
        return {"error": "Modèle non chargé. Vérifiez les logs backend."}

    print(f"🚀 Modèle utilisé : {type(model)}")  # Debugging du type du modèle

    try:
        if not hasattr(model, "predict"):
            raise AttributeError(f"⚠️ L'objet modèle {type(model)} ne possède pas de méthode `predict()`")

        prediction = model.predict([data.features])
        return {"prediction": prediction.tolist()}
    except Exception as e:
        print(f"❌ Erreur lors de la prédiction : {str(e)}")
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}
