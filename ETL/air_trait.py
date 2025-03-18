
import pandas as pd
# Importer la fonction get_mongo_data depuis connexion_mongo
from connexion_mongo import get_mongo_data

# Récupérer les DataFrames retournés par la fonction
df_vie, df_air, df_resp = get_mongo_data()  # Assurez-vous que get_mongo_data() retourne trois DataFrames

# Convertir la colonne 'date' en format datetime (en prenant en compte le format jour/mois/année)
try:
    df_air['date'] = pd.to_datetime(df_air['date'], dayfirst=True)
    print("\nLa colonne 'date' a été convertie avec succès.")
except Exception as e:
    print(f"\nErreur lors de la conversion de la colonne 'date': {e}")

# Extraire l'année et l'ajouter comme nouvelle colonne 'annee'
df_air['annee'] = df_air['date'].dt.year

"""# Gérer les valeurs NaN  et les remplacer par 0 ou supprimer les lignes avec des Nan
df_air['annee'] = df_air['annee'].fillna(0).astype(int)

# Gérer les valeurs infinies dans 'annee' (si existantes)
df_air['annee'] = df_air['annee'].replace([float('inf'), float('-inf')], float('nan')).fillna(0).astype(int)"""

# Filtrer les données pour les années entre 2020 et 2025
df_air_quality_filtered = df_air[(df_air['annee'] > 2020) & (df_air['annee'] < 2025)]

# Extraire le mois et l'ajouter comme nouvelle colonne 'mois'
df_air['mois'] = df_air['date'].dt.month

# Afficher les premières lignes du DataFrame pour vérifier les modifications
print("\nPremières lignes du DataFrame après modification:")
print(df_air.head())

# Regroupement des valeurs de la qualité de l'air par mois ,anné et région en calculant la moyenne des valeurs
df_grouped = df_air.groupby(['mois', 'annee', 'region']).agg({
    'pm10': 'mean',
    'pm2_5': 'mean',
    'carbon_monoxide': 'mean',
    'nitrogen_dioxide': 'mean',
    'sulphur_dioxide': 'mean',
    'ozone': 'mean',
    'grass_pollen': 'mean',
}).reset_index()

# Afficher les résultats du regroupement
print("\nDonnées regroupées par année, mois et région avec les moyennes:")
print(df_grouped.head())

# Sauvegarder le DataFrame regroupé dans un fichier CSV (optionnel)
# df_grouped.to_csv("C:/santé et comportement/tables/air_quality_grouped.csv", index=False)

