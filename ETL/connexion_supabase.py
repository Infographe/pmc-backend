import pandas as pd
import psycopg2
from psycopg2 import sql
import logging
import transformation_data
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER_SB,
        password=PASSWORD_SB,
        host=HOST_SB,
        port=PORT_SB,
        dbname=DBNAME_SB
    )
    print("Connection successful!")


# Configuration du logging permet de donner des infos de connexion
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


# Création d'un curseur
cur = conn.cursor()

df=transformation_data.df_imputed

# Convertir les colonnes de type numérique en float si nécessaire
numeric_columns = df.columns.difference(["patho_niv1"])
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Insérer les données dans la table 'pmc'
for index, row in df.iterrows():
    try:
        # Construire la requête d'insertion
        insert_query = sql.SQL("""
            INSERT INTO pmc (
                sexeps, fqcantine, entrerep, fastfood, enrich, cyclepds, enceinte, allaite,
                menopaus, ths, fume, agefumem, dlcpl, contmed, contsubt, fqvpo, fqpl, pasreg,
                acolmat1_gr, acolmat2_gr, acolmat3_gr, acolmat4_gr, agglo9, situ_mat, situ_prof,
                heur_trav, trav_nuit, typ_empl, stat_empl, vacances, region, dip, bmi, statnut,
                ipaq, taille, saison, typelait, annee, patho_niv1, cla_age_5, dept, ntop, npop, prev,
                mois, pm10, pm2_5, carbon_monoxide, nitrogen_dioxide, sulphur_dioxide, ozone, grass_pollen,
                ajout_sel, temps_act_phy, p_animal, p_vegetale, gras_animal, vistes_medecins, fumeur,
                sedentaire, regime_special, achats_distributeurs, poids_moyen
            ) VALUES (
                %(sexeps)s, %(fqcantine)s, %(entrerep)s, %(fastfood)s, %(enrich)s, %(cyclepds)s, %(enceinte)s,
                %(allaite)s, %(menopaus)s, %(ths)s, %(fume)s, %(agefumem)s, %(dlcpl)s, %(contmed)s, %(contsubt)s,
                %(fqvpo)s, %(fqpl)s, %(pasreg)s, %(acolmat1_gr)s, %(acolmat2_gr)s, %(acolmat3_gr)s, %(acolmat4_gr)s,
                %(agglo9)s, %(situ_mat)s, %(situ_prof)s, %(heur_trav)s, %(trav_nuit)s, %(typ_empl)s, %(stat_empl)s,
                %(vacances)s, %(region)s, %(dip)s, %(bmi)s, %(statnut)s, %(ipaq)s, %(taille)s, %(saison)s,
                %(typelait)s, %(annee)s, %(patho_niv1)s, %(cla_age_5)s, %(dept)s, %(ntop)s, %(npop)s, %(prev)s,
                %(mois)s, %(pm10)s, %(pm2_5)s, %(carbon_monoxide)s, %(nitrogen_dioxide)s, %(sulphur_dioxide)s,
                %(ozone)s, %(grass_pollen)s, %(ajout_sel)s, %(temps_act_phy)s, %(p_animal)s, %(p_vegetale)s,
                %(gras_animal)s, %(vistes_medecins)s, %(fumeur)s, %(sedentaire)s, %(regime_special)s,
                %(achats_distributeurs)s, %(poids_moyen)s
            )
        """)

        # Convertir la ligne en dictionnaire pour l'insertion
        row_dict = row.to_dict()

        # Exécuter la requête d'insertion
        cur.execute(insert_query, row_dict)

        # Log de succès pour chaque ligne insérée
        logger.info(f"Ligne {index+1}/{len(df)} insérée avec succès.")

    except Exception as e:
        logger.error(f"Erreur lors de l'insertion de la ligne {index+1}: {e}")

# Valider les changements
try:
    conn.commit()
    logger.info("Toutes les données ont été insérées et les changements validés.")
except Exception as e:
    logger.error(f"Erreur lors de la validation des changements : {e}")

# Fermer la connexion
cur.close()
conn.close()

logger.info("Connexion à la base de données fermée.")