from models import AverageModel
import dill
import os

# Créer une instance du modèle
model = AverageModel()

# Vérifier si le dossier 'models' existe, sinon le créer
if not os.path.exists("models"):
    os.makedirs("models")

# Sauvegarder le modèle au format .pkl
model_path = "models/average_model.pkl"

with open(model_path, "wb") as f:
    dill.dump(model, f)

print(f"✅ Modèle sauvegardé avec succès dans {model_path} !")
