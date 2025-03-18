import dill
import numpy as np

# Chemin du modèle
ml_model_path = "models/LightGBM_best_model_2.pkl"

# Chargement
with open(ml_model_path, "rb") as f:
    model = dill.load(f)

# Test avec des valeurs arbitraires
features = np.array([[111, 30, 166, 195, 288, 10, 20, 0.5, 1, 0, 70, 80, 90, 60, 100, 150, 2, 4, 8, 15, 12, 150, 25, 30, 40, 5, 8, 3, 9, 7]])
prediction = model.predict(features)

print(f"✅ Prédiction réussie : {prediction}")
