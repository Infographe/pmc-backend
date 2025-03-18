import requests
import requests_cache
from datetime import datetime
import pandas as pd
import json
from dotenv import load_dotenv
import time

import os

uri = "https://fair.healthinformationportal.eu/dataset/a8832b77-2075-400a-93b2-35d974261f80"
headers = {'Accept': 'text/turtle'}
res = requests.get(url=uri, headers=headers) 
# print(res.text) 

csv_filename = "air_quality_results.csv"
first_export = True  # Pour écrire l'en-tête lors de la première exportation


# Liste des villes
cities = [
    "Bourg-en-Bresse", "Laon", "Moulins", "Digne-les-Bains", "Gap",
    "Nice", "Privas", "Charleville-Mezières", "Foix", "Troyes",
    "Carcassonne", "Rodez", "Marseille", "Caen", "Aurillac",
    "Angouleme", "La Rochelle", "Bourges", "Tulle", "Ajaccio",
    "Bastia", "Dijon", "Nantes", "Gueret", "Perigueux",
    "Besancon", "Valence", "Evreux", "Chartres", "Quimper",
    "Nîmes", "Toulouse", "Auch", "Bordeaux", "Montpellier",
    "Rennes", "Châteauroux", "Tours", "Grenoble", "Lons-le-Saunier",
    "Mont-de-Marsan", "Blois", "Saint-Etienne", "Le Puy-en-Velay",
    "Nantes", "Orleans", "Cahors", "Agen", "Mende",
    "Angers", "Saint-Lo", "Châlons-en-Champagne", "Chaumont", "Laval",
    "Nancy", "Bar-le-Duc", "Vannes", "Metz", "Nevers",
    "Lille", "Beauvais", "Alencon", "Arras", "Clermont-Ferrand",
    "Pau", "Tarbes", "Perpignan", "Strasbourg", "Colmar",
    "Lyon", "Vesoul", "Macon", "Le Mans", "Chambery",
    "Annecy", "Paris", "Rouen", "Melun", "Versailles",
    "Niort", "Amiens", "Albi", "Montauban", "Toulon",
    "Avignon", "La Roche-sur-Yon", "Poitiers", "Limoges", "Epinal",
    "Auxerre", "Belfort", "Evry", "Nanterre", "Bobigny",
    "Creteil", "Pontoise"
]

i = 0
################################ Departement #################################
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
for city in cities:
    # Liste pour accumuler les DataFrames quotidiens de chaque ville
    all_daily_dataframes = []

    i = i+1
    dep_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=fr&format=json"

    response = cache_session.get(dep_url)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

    dep = response.text
    parsed_data = json.loads(dep)
    results = parsed_data.get("results", [])

    if results:
        for r in results:
            if r['country_code'] == "FR" and r['country'] == "France":
                latitude = r["latitude"]
                longitude = r["longitude"]
                region = r.get('admin1', 'Region inconnu')
                depName = r.get('admin2', 'Département inconnu')
            else:
                print(f"La ville {city} n'est peut-être pas en France.")
                # print("La cle 'results' n'a pas ete trouvee.")
    print(f"city => {city} , département => {depName}")
    ### ne pas surcharger l'API (60s)
    if i % 2 == 0:
        time.sleep(61)
        continue
    # ################################ Air quality #################################
    db_url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    # Initialisation de la session de cache
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)

    # Configuration de l'URL de l'API et des paramètres
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "pm10", "pm2_5", "carbon_monoxide", 
            "nitrogen_dioxide", "sulphur_dioxide", 
            "ozone"
            # "ozone", "grass_pollen"
        ],
        "timezone": "Europe/Moscow",
        "start_date": "2016-01-02",
        "end_date": "2025-02-02",
    }

    # Recuperation des donnees de l'API
    response = cache_session.get(db_url, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}, {response.text}")

    # Extraction des donnees horaires
    data = response.json().get("hourly", {})
    time_intervals = data.pop("time", [])

    # Creation d'un DataFrame directement
    hourly_dataframe = pd.DataFrame({
        "time": [datetime.fromisoformat(t) for t in time_intervals],
        **{key: data[key] for key in data.keys() if key in params["hourly"]}
    })

    # Traitement des colonnes
    hourly_dataframe["time"] = pd.to_datetime(hourly_dataframe["time"], errors="coerce")
    hourly_dataframe.dropna(subset=["time"], inplace=True)  # Supprimer les valeurs invalides
    hourly_dataframe["date"] = hourly_dataframe["time"].dt.date

    # Regrouper par jour et calculer les moyennes, puis arrondir à 2 decimales
    daily_dataframe = hourly_dataframe.groupby("date").mean().round(2).reset_index()

    # Fonction de classification de la qualite de l'air
    def classify_air_quality(row):
        thresholds = {
            "pm10": [20, 50, 100, 250],
            "pm2_5": [10, 25, 50, 75],
            "ozone": [50, 100, 180, 240],
            "nitrogen_dioxide": [40, 100, 200, 400],
            "sulphur_dioxide": [20, 80, 250, 500],
            "carbon_monoxide": [4, 9, 12, 15],
            # "grass_pollen": 50,
        }
        
        air_quality = "Bonne"
        try:
            row = row.fillna(0)  # Remplacer les NaN par 0
            if row["pm10"] >= thresholds["pm10"][3] or row["pm2_5"] >= thresholds["pm2_5"][3]:
                air_quality = "Dangereuse"
            elif row["pm10"] >= thresholds["pm10"][2] or row["pm2_5"] >= thresholds["pm2_5"][2]:
                air_quality = "Très mauvaise"
            elif row["ozone"] >= thresholds["ozone"][2] or row["nitrogen_dioxide"] >= thresholds["nitrogen_dioxide"][2]:
                air_quality = "Mauvaise"
            elif row["pm10"] >= thresholds["pm10"][1] or row["pm2_5"] >= thresholds["pm2_5"][1]:
                air_quality = "Moderee"
            # elif row["grass_pollen"] >= thresholds["grass_pollen"]:
            #     air_quality = "Acceptable avec risques d'allergie"
            elif row["pm10"] >= thresholds["pm10"][0] or row["pm2_5"] >= thresholds["pm2_5"][0]:
                air_quality = "Acceptable"
        except KeyError as e:
            print(f"Cle manquante : {e}")
        return air_quality

    # Appliquer la classification de la qualite de l'air
    daily_dataframe["air_quality"] = daily_dataframe.apply(classify_air_quality, axis=1)
    daily_dataframe["region"] = region
    daily_dataframe["departement"] = depName
    daily_dataframe["ville"] = city
    
    print("dept :", i, daily_dataframe)
    
    if not daily_dataframe.empty:
        if first_export:
            daily_dataframe.to_csv(csv_filename, index=False, encoding="utf-8-sig")
            first_export = False
        else:
            daily_dataframe.to_csv(csv_filename, mode='a', index=False, header=False, encoding="utf-8-sig")

