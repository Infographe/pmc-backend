import pandas as pd
from connexion_mongo import get_mongo_data
import air_trait  

# Appeler la fonction get_mongo_data pour récupérer les DataFrames
df_vie, df_resp, df_air = get_mongo_data()

# Assurez-vous que df_grouped existe bien dans air_trait
df_air_g= air_trait.df_grouped

# Vérifier les noms des colonnes pour chaque DataFrame
print("Colonnes de df_air:", df_air_g.columns)
print("Colonnes de df_vie:", df_vie.columns)
print("Colonnes de df_resp:", df_resp.columns)

# Spécifier les types de données pour chaque DataFrame
dtype_df_vie = {'region': 'int', 'agepmin': 'float64', 'agncuis': 'float64', 'alimpub1': 'object', 'alimpub2': 'object',
                'alimpub3': 'object', 'alimpub4': 'object', 'alimpub5': 'object', 'alimpub6': 'object',
                'aptotal_hebdo': 'float64', 'assis_j': 'float64', 'autlieudej': 'object', 'boeufcru': 'float64',
                'boeufcuis': 'float64', 'bonalim': 'float64', 'chevcru': 'float64', 'chevcuis': 'float64',
                'clage': 'float64', 'cotagncuis': 'float64', 'cspi': 'float64', 'cyclepds': 'float64',
                'distrib': 'float64', 'dlcpl': 'float64', 'enrich': 'float64', 'entrerep': 'float64',
                'essaipds': 'float64', 'etiquetad': 'float64', 'fastfood': 'float64', 'foiecuis': 'float64',
                'fqcantine': 'float64', 'fqfec': 'float64', 'fqfl': 'float64', 'fqpl': 'float64', 'fqvpo': 'float64',
                'fume': 'float64', 'infoami': 'float64', 'infoaut': 'float64', 'infofami': 'float64',
                'infointern': 'float64', 'infolivre': 'float64', 'infomed': 'float64', 'infopharm': 'float64',
                'infopress': 'float64', 'infoprof': 'float64', 'infopub': 'float64', 'infotele': 'float64',
                'intaliaut': 'float64', 'intalicuisi': 'float64', 'intalifabr': 'float64', 'intaliform': 'float64',
                'intalim': 'float64', 'intalinouv': 'float64', 'intaliplais': 'float64', 'intaliregi': 'float64',
                'intense_hebdo': 'float64', 'intense_j': 'float64', 'intense_met': 'float64', 'intense_nbJ': 'float64',
                'ipaq': 'float64', 'lardcru': 'float64', 'lieudej': 'float64', 'marche_hebdo': 'float64',
                'marche_j': 'float64', 'marche_nbJ': 'float64', 'modere_hebdo': 'float64', 'modere_j': 'float64',
                'modere_met': 'float64', 'modere_nbJ': 'float64', 'nbgeneral': 'float64', 'nbspecial': 'float64',
                'oeufcru': 'float64', 'opipoids': 'float64', 'pdsmax': 'float64', 'pdsmin': 'float64',
                'poids12': 'float64', 'poiscru': 'float64', 'porccru': 'float64', 'porccuis': 'float64', 'q148': 'float64',
                'regimedj': 'float64', 'regimem': 'float64', 'rotboeufcuis': 'float64', 'sauccru': 'float64',
                'sauccuis': 'float64', 'selassent': 'float64', 'selassfec': 'float64', 'selassleg': 'float64',
                'selassoeuf': 'float64', 'selassvp': 'float64', 'selassvps': 'float64', 'sexeps': 'float64',
                'shboeufcuis': 'float64', 'stat_empl': 'float64', 'statnut': 'float64', 'taille': 'float64',
                'total_nbj': 'float64', 'typ_empl': 'float64', 'v2_nbenf': 'float64', 'veaucuis': 'float64',
                'voeupoids': 'float64', 'volcru': 'float64', 'volcuis': 'float64'}

dtype_df_resp = {'region': 'int', 'Ntop': 'float64', 'dept': 'object', 'annee': 'int'}
dtype_df_air_g = {'region': 'int'}

# Convertir les colonnes 'region' des 3 DataFrames en int
df_vie['region'] = df_vie['region'].astype(int)
df_air_g['region'] = df_air_g['region'].astype(int)
df_resp['region'] = df_resp['region'].astype(int)

# Vérification des valeurs manquantes et doublons dans la colonne 'region'
print("Valeurs manquantes dans df_vie['region']:", df_vie['region'].isnull().sum())
print("Doublons dans df_vie['region']:", df_vie['region'].duplicated().sum())

print("Valeurs manquantes dans df_air['region']:", df_air_g['region'].isnull().sum())
print("Doublons dans df_air['region']:", df_air_g['region'].duplicated().sum())

print("Valeurs manquantes dans df_resp['region']:", df_resp['region'].isnull().sum())
print("Doublons dans df_resp['region']:", df_resp['region'].duplicated().sum())

# Fusionner df_vie et df_resp sur la colonne 'region'
df_vie_resp = pd.merge(df_vie, df_resp, on='region', how='outer')  # 'how' peut être 'left', 'right', 'inner', 'outer'

# Optimiser les types de données des colonnes pour réduire la mémoire utilisée
df_vie_resp = df_vie_resp.astype({'region': 'int32'})
df_air_g = df_air.astype({'region': 'int32'})

# Fusionner df_vie_resp et df_air sur la colonne 'region' et 'annee'
df_merge_tot = pd.merge(df_vie_resp, df_air_g, on=['region', 'annee'], how='left')

# Enregistrer le DataFrame fusionné dans un fichier CSV
df_merge_tot.to_csv('join_total1.csv', index=False)

# Afficher les premières lignes du DataFrame fusionné
print("Résultat de la fusion :")
print(df_merge_tot.head())
