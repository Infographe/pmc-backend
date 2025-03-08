import pickle

# Définir une classe pour calculer la moyenne
class AverageModel:
    def predict(self, X):
        """
        Prend une liste ou un tableau de données et renvoie la moyenne pour chaque échantillon.
        :param X: Liste de listes ou tableau 2D où chaque sous-liste contient 5 features.
        :return: Liste des moyennes.
        """
        return [sum(features) / len(features) for features in X]

# Créer une instance du modèle
model = AverageModel()

# Sauvegarder le modèle au format pkl
with open('average_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Modèle sauvegardé sous le nom 'average_model.pkl'")
