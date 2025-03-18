import pandas as pd
import time  # Ajouter l'importation du module time
from pymongo import MongoClient
import configparser

# Créer une instance du parser
config = configparser.ConfigParser()

# Charger le fichier config.ini
config.read('config.ini')

# Récupérer les informations d'identification depuis le fichier config.ini
db_user = config['cluster0']['user']
db_password = config['cluster0']['password']
db_name = config['cluster0']['database_name']

# Construire l'URI MongoDB pour se connecter
mongo_uri = f"mongodb+srv://{db_user}:{db_password}@cluster0.fhy27.mongodb.net/{db_name}?retryWrites=true&w=majority"

# Fonction pour récupérer les données par lots avec un lot plus petit et gestion des exceptions
def fetch_data_in_batches(collection, filter_query=None, batch_size=25):
    batch_number = 0
    while True:
        try:
            # Récupérer les lots avec pagination
            cursor = collection.find(filter_query).skip(batch_number * batch_size).limit(batch_size)
            batch = list(cursor)

            # Si aucun lot n'est trouvé, on sort de la boucle
            if not batch:
                break
            yield pd.DataFrame(batch)

            # Passer au lot suivant
            batch_number += 1
        except Exception as e:
            print(f"Erreur de connexion : {e}, tentative de reconnection en cours...")
            time.sleep(5)  # Attendre avant de réessayer


# Fonction pour concaténer les lots en un seul DataFrame
def concatenate_batches(collection):
    df_list = []
    for batch in fetch_data_in_batches(collection):
        df_list.append(batch)
    return pd.concat(df_list, ignore_index=True)


# Fonction pour récupérer les trois DataFrames
def get_mongo_data():
    # Connexion à MongoDB avec l'URI
    client = MongoClient(mongo_uri)

    # Accéder à la base de données
    db = client['Projet_Maladies_Chroniques']

    # Afficher ou utiliser le lien de connexion
    print("MongoDB Connection URI:", mongo_uri)

    # Récupérer les données des trois collections
    collection_vie = db['mode_de_vie']
    collection_air = db['qualite_air']
    collection_resp = db['Maladie_respiratoire']

    # Transformer les collections en DataFrames
    df_vie = concatenate_batches(collection_vie)
    df_air = concatenate_batches(collection_air)
    df_resp = concatenate_batches(collection_resp)

    # Retourner les trois DataFrames
    return df_vie, df_air, df_resp


# Appeler la fonction pour récupérer les DataFrames
df_vie, df_air, df_resp = get_mongo_data()

# Afficher les premières lignes des DataFrames pour vérifier
print(df_vie.head())  # Vérifier les premières lignes du DataFrame mode de vie
print(df_air.head())  # Vérifier les premières lignes du DataFrame qualité de l'air
print(df_resp.head())  # Vérifier les premières lignes du DataFrame maladie respiratoire
