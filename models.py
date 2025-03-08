class AverageModel:
    def predict(self, X):
        """
        Prend une liste ou un tableau 2D en entrée et retourne la moyenne pour chaque échantillon.
        """
        return [sum(features) / len(features) for features in X]
