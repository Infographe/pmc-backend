import pandas as pd
import dask.dataframe as dd
from pymongo import MongoClient
import time
import gc
from dask.distributed import Client

if __name__ == '__main__':
    client = Client(timeout='120s')  # Augmenter le délai d'attente à 120 secondes
    print(client)

    # Fonction pour récupérer les données par lots avec un lot plus petit et gestion des exceptions
    def fetch_data_in_batches(collection, filter_query=None, batch_size=25):
        batch_number = 0
        while True:
            try:
                cursor = collection.find(filter_query).skip(batch_number * batch_size).limit(batch_size)
                batch = list(cursor)
                if not batch:
                    break
                yield pd.DataFrame(batch)
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

    # Connexion à MongoDB
    client = MongoClient('mongodb+srv://Fatma:u9tAq3uZPUcD15Uy@cluster0.fhy27.mongodb.net/Projet_Maladies_Chroniques?retryWrites=true&w=majority&authSource=admin')
    db = client['Projet_Maladies_Chroniques']
    collection = db['mode_de_vie']
    collection1 = db['qualite_air']
    collection2 = db['Maladie_respiratoire']

    # Transformer les collections en DataFrames Dask après filtrage et augmenter le nombre de partitions
    df = dd.from_pandas(concatenate_batches(collection), npartitions=25)
    df1 = dd.from_pandas(concatenate_batches(collection1), npartitions=25)
    df2 = dd.from_pandas(concatenate_batches(collection2), npartitions=25)

    # S'assurer que les clés de jointure sont du même type
    df['region'] = df['region'].astype(str)
    df1['region_num'] = df1['region_num'].astype(str)
    df2['region'] = df2['region'].astype(str)

    # Jointure des DataFrames avec Dask
    df_air_vie = dd.merge(df, df1, left_on='region', right_on='region_num').persist()

    # Jointure finale avec Dask
    df_total = dd.merge(df_air_vie, df2, left_on='region_num', right_on='region')

    # Nettoyer les objets inutilisés pour libérer de la mémoire
    del df
    del df1
    del df2
    del df_air_vie
    gc.collect()

    # Exportation du DataFrame final en un seul fichier CSV avec compression
    df_total.to_csv('jointure_totale_combine.csv', single_file=True, index=False, compression='gzip', blocksize="256MB")

