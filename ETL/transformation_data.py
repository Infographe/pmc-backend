import pandas as pd
from connexion_mongo import get_mongo_data
import numpy as np
import jointure

#importation des données (sortie jointure)
df=jointure.df_merge_tot

#élimination des valeurs abberante de Ntop
# Calculer l'IQR pour 'Ntop'
Q1 = df['Ntop'].quantile(0.25)
Q3 = df['Ntop'].quantile(0.75)
IQR = Q3 - Q1
print("Q1:", Q1, "Q3:", Q3, "IQR:", IQR)

# Identifier et éliminer les valeurs aberrantes
df = df[~((df['Ntop'] < (Q1 - 1.5 * IQR)) | (df['Ntop'] > (Q3 + 1.5 * IQR)))]






#Regroupement de data (consommation de sucre)
df['conso_sucre'] = np.where(
    (df['suc_yao'].isin([1, 2, 3, 7, 9])) |
    (df['suc_froblanc'].isin([1, 2, 3, 7, 9])) |
    (df['suc_suisse'].isin([1, 2, 3, 7, 9])) |
    (df['suc_cafe'].isin([1, 2, 3, 7, 9])) |
    (df['suc_the'].isin([1, 2, 3, 7, 9])) |
    (df['suc_boischoc'].isin([1, 2, 3, 7, 9]))|
    (df['suc_the'].isin([1, 2, 3, 7, 9]))
                            ,
    1,  # si l'un des types de sucres est consommé
    0   # aucune consommation de sucre
)

# regroupement des entre_repas
df['entrerep'] = df['entrerep'] + df['colmata']


#Regroupement de data (ajout sel)
df['ajout_sel'] = np.where(
    (df['selassent'].isin([1, 2, 3,4])) |
    (df['selassleg'].isin([1, 2, 3,4])) |
    (df['selassfec'].isin([1, 2, 3,4])) |
    (df['selassvp'].isin([1, 2, 3,4])) |
    (df['selassvps'].isin([1, 2, 3,4])) |
    (df['selassoeuf'].isin([1, 2, 3,4])),
    1,  # s'il y a ajout de sel dans les repas
    0   # pas d'ajout de sel
)
#activité_physique
df.columns = df.columns.str.strip()
df['temps_act_phy'] = df[['intense_hebdo', 'modere_hebdo', 'marche_hebdo', 'aptotal_hebdo']].mean(axis=1) * 7 / 60

#valeurs proteines
select_columns = ["boeufcru", "chevcru", "porccru", "volcru", "poiscru", "oeufcru",
                "shboeufcuis", "boeufcuis", "rotboeufcuis", "foiecuis", "veaucuis",
                "porccuis", "sauccuis", "chevcuis", "agncuis", "volcuis","lardcru","sauccru"]
df["p_animal"] = df[select_columns].sum(axis=1)
df["p_vegetale"] = df[["fqfec", "fqfl"]].sum(axis=1)
df['gras_animal'] = df['peaupoulet'] + df['grasjambon']
df['vistes_medecins'] = df['nbgeneral'] + df['nbspecial']

nb_cig_jours = ["nbcigrjm", "nbpipejm", "nbcigtm", "nbcigrja", "nbpipeja", "nbcigta"]
nb_cig_semaine = ["nbpipesm", "nbcigrsm", "nbpipesa", "nbcigrsa"]

# Convertir par semaine (consommation de cigarettes)
convert_to_semaine = df[nb_cig_jours].mul(7)

# Sélectionner les colonnes pour la semaine
semaine_df = df[nb_cig_semaine]

# Concaténer et calculer la moyenne
df["fumeur"] = pd.concat([convert_to_semaine, semaine_df], axis=1).mean(axis=1)
#calcul de la sédentaire
df["sedentaire"] = df[["tele", "ordi", "sed",'assis_j']].mean(axis=1)*7/60
# --------------- Régime spécial --------------------
select_columns = ["regimem", "regimedj", "regvegr", "regvegt", "regrelig",
                "regmedic", "regform", "regstab", "regmaig", "regaut"]
df["regime_special"] = df[select_columns].sum(axis=1)
#Achats distributeur
select_distr = ["distconf","distfruit","distsoli","disteaum","distsoda","distjus","distbar","distgat","distbiss","distaut"]
df["achats_distributeurs"] = df[select_distr].sum(axis=1)





#suppression des colonnes répétitives et après regroupements
df = df.drop(['libelle_sexe', 'niveau_prioritaire', 'sexe', 'top', 'chef', 'up', 'tage', 'v2_age', 'cible','tri','v2_age','cible','pond_adu_ech','q148','lieudej','clage','lieudej','loc_log','lien_int_chef','nrentr','nrcont','pdsmaxnsp','moisgross','nbpipemnsp','nrentr','contap','agepmin','nrreg','nrcont','pdsmaxnsp','moisgross','nbpipemnsp','nrentr','v2_nbenf','reg','Niveau prioritaire','acolmat1_cod','acolmat2_cod','acolmat3_cod','acolmat4_cod','nbpipemnsp','enceinte12'], axis=1, errors='ignore')
df = df.drop(['conso_sucre', 'suc_yao', 'suc_froblanc', 'suc_suisse', 'suc_cafe', 'suc_boischoc','suc_the'], axis=1, errors='ignore')
df.drop(['colmata'], axis=1, errors='ignore')
df = df.drop(['selassent', 'selassleg', 'selassfec', 'selassvp', 'selassvps', 'selassoeuf','colmata'], axis=1, errors='ignore')
df = df.drop(['intense_nbJ', 'modere_nbJ', 'marche_nbJ', 'intense_hebdo', 'modere_hebdo',
              'marche_hebdo', 'intense_j', 'modere_j', 'marche_j', 'modere_met', 'marche_met',
              'aptotal_met', 'total_nbj','aptotal_hebdo','act_phy'], axis=1, errors='ignore')
df = df.drop(['moisgrossnsp', 'nbcigrmnsp', 'agefumemnsp','nbcigransp','nbpipeansp','nbpipeansp','nbpipeansp','cantsant','colmatecol','fqcigta','agefumea','agefumeansp','agestop','agestopnsp','fqcigtm'], axis=1, errors='ignore')
df = df.drop(['infoami', 'infoaut', 'intaliaut','intalicuisi', 'intalifabr','intaliform','intaliplais','intaliregi','acolmat1','acolmat2','acolmat3','acolmat4'], axis=1, errors='ignore')
df.drop(columns=select_columns, inplace=True)
df.drop(columns=["fqfec", "fqfl"], inplace=True)
df.drop(['peaupoulet', 'grasjambon'], axis=1, inplace=True)
df.drop(['nbgeneral', 'nbspecial'], axis=1, inplace=True)
drop_cols = nb_cig_jours + nb_cig_semaine
df.drop(columns=drop_cols, inplace=True)
df.drop(columns=["tele", "ordi", "sed",'assis_j'], inplace=True)
df.drop(columns=select_columns, inplace=True)
df.drop(columns=select_distr, inplace=True)

#####################################imputations des valeurs manquantes_most_frequent####################################

from sklearn.impute import SimpleImputer

# Créer l'objet SimpleImputer avec la stratégie 'most_frequent'
simple_most = SimpleImputer(strategy='most_frequent')



# Appliquer l'imputation à la colonne 'entrerep' et remplacer les valeurs manquantes

df.columns = df.columns.str.strip()

# Sélectionner les colonnes à imputer
data_freq = df[['entrerep','sexeps', 'ajout_sel', 'heur_trav', 'trav_nuit', 'ths', 'acolmat1_gr', 'acolmat2_gr', 'acolmat3_gr', 'acolmat4_gr', 'contmed','ipaq','dlcpl','fqvpo','fqpl','typ_empl','stat_empl','statnut', 'cla_age_5', 'dept','fqcantine','fastfood', 'enrich','agefumem','fume','annee','mois','contsubt','vistes_medecins']]

# Appliquer l'imputation sur les colonnes sélectionnées
df[['entrerep','sexeps', 'ajout_sel', 'heur_trav', 'trav_nuit', 'ths', 'acolmat1_gr', 'acolmat2_gr', 'acolmat3_gr', 'acolmat4_gr', 'contmed','ipaq','dlcpl','fqvpo','fqpl','typ_empl','stat_empl','statnut', 'cla_age_5', 'dept','fqcantine','fastfood', 'enrich','agefumem','fume','annee','mois','contsubt','vistes_medecins']] = simple_most.fit_transform(data_freq)


"********************************************imputations des valeurs manquantes_moyenne*****************************************************************"
df.columns = df.columns.str.strip()
# Sélection des colonnes numériques
data_numerique = df[['sedentaire', 'temps_act_phy']]

# Création de l'imputer avec la stratégie 'mean' (moyenne)
imputer_mean = SimpleImputer(strategy='mean')

# Appliquer l'imputation par la moyenne sur les colonnes sélectionnées
df[['sedentaire', 'temps_act_phy']] = imputer_mean.fit_transform(data_numerique)

"*********************************"
# Sélectionner les colonnes à imputer
data_pop = df[['Ntop', 'prev', 'Npop']]

# Appliquer l'imputation par la moyenne
df[data_pop.columns] = imputer_mean.fit_transform(data_pop)




"*********************Remplacement des nanpar 0********************************"
df['fumeur'] = df['fumeur'].fillna(0)
df['pasreg']= df['pasreg'].fillna(0)
"************************************"
# Sélectionner les colonnes à traiter
data_femme = df[['enceinte', 'allaite', 'menopaus']]

# Appliquer fillna pour remplacer les valeurs manquantes par 0
df[['enceinte', 'allaite','menopaus']] = data_femme.fillna(0)

#***************************Transformations des données du poids********************************
# Liste des colonnes contenant les données sur le poids
data_poids = ['poids12', 'pdsmax', 'pdsmin', 'poidsm', 'poids']

# Remplacer les valeurs 998 et 999 par 99 dans les colonnes concernées
df[data_poids] = df[data_poids].replace({998: 99, 999: 99})

# Calculer la moyenne des colonnes
df['poids_moyen'] = df[data_poids].mean(axis=1)

"***********Imputation poids après transformations*************"

# Appliquer l'imputation par groupe d'âge (cla_age_5)
for group in df['cla_age_5'].unique():  # Pour chaque groupe d'âge unique
    # Sélectionner les lignes de ce groupe
    group_data = df[df['cla_age_5'] == group]

    # Appliquer l'imputation sur les colonnes d'intérêt pour ce groupe
    df.loc[df['cla_age_5'] == group, ['poids_moyen', 'cyclepds', 'taille']] = imputer_mean.fit_transform(
        group_data[['poids_moyen', 'cyclepds', 'taille']])

# Vérification : afficher les premières lignes pour s'assurer que l'imputation a été faite

# Calcul des valeurs manquantes de IMC


# Calculer le BMI pour les lignes où 'bmi' est manquant (NaN)
df.loc[df['bmi'].isna(), 'bmi'] = df.loc[df['bmi'].isna(), 'poids_moyen'] / np.square(df.loc[df['bmi'].isna(), 'taille'])

#******************************************Imputations des valeurs de la qualité de l'air***********************************************************
# Etape 1
from sklearn.impute import SimpleImputer

# Liste des colonnes à imputer
data_air = ['pm10', 'pm2_5', 'carbon_monoxide', 'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'grass_pollen']

# Créer l'objet SimpleImputer avec la stratégie 'median'
imputer_simple_air = SimpleImputer(strategy='median')

# Créer un DataFrame vide pour les résultats imputés
df_imputed = df.copy()

# Grouper les données par 'region', 'mois', et 'annee'
df_grouped = df_imputed.groupby(['region', 'mois', 'annee'])

# Appliquer l'imputation SimpleImputer pour chaque groupe
for group, group_data in df_grouped:
    # Appliquer l'imputation uniquement si le groupe contient des données manquantes
    if group_data[data_air].isnull().any().any():
        # Séparer les colonnes avec toutes les valeurs manquantes
        cols_with_all_missing = group_data[data_air].columns[group_data[data_air].isnull().all()]
        cols_with_some_values = group_data[data_air].columns.difference(cols_with_all_missing)

        # Appliquer l'imputation sur les colonnes avec des valeurs observées
        if not cols_with_some_values.empty:
            transformed_values = imputer_simple_air.fit_transform(group_data[cols_with_some_values])

            # Vérification : transformed_values doit avoir les mêmes dimensions que group_data[cols_with_some_values]
            assert transformed_values.shape == group_data[
                cols_with_some_values].shape, "Les dimensions ne correspondent pas !"

            # Affecter les valeurs imputées au DataFrame df_imputed
            df_imputed.loc[group_data.index, cols_with_some_values] = transformed_values

#Etape 2
# Créer l'objet SimpleImputer avec la stratégie 'mean'
imputer_simple_air2 = SimpleImputer(strategy='median')
df_imputed[data_air]= imputer_simple_air2.fit_transform(df_imputed[data_air])

# Créer SimpleImputer avec la stratégie 'mean'
imputer_simple_air2 = SimpleImputer(strategy='mean')

# Appliquer l'imputation sur les colonnes spécifiées
df_imputed[data_air] = imputer_simple_air2.fit_transform(df_imputed[data_air])


#*******************************************Encodage des données***************************************************
from sklearn.preprocessing import LabelEncoder

# Initialiser un encodeur
label_encoder = LabelEncoder()

# Liste des colonnes catégorielles
categorical_columns = [
    'sexeps', 'fqcantine', 'entrerep', 'fastfood', 'enrich', 'cyclepds',
    'enceinte', 'allaite', 'menopaus', 'ths', 'fume', 'agefumem', 'dlcpl',
    'contmed', 'contsubt', 'fqvpo', 'fqpl', 'pasreg', 'acolmat1_gr',
    'acolmat2_gr', 'acolmat3_gr', 'acolmat4_gr', 'agglo9', 'situ_mat',
    'situ_prof', 'trav_nuit', 'typ_empl', 'stat_empl',
    'vacances', 'region', 'dip', 'statnut', 'ipaq',
    'saison', 'typelait', 'annee', 'cla_age_5', 'dept',
    'mois', 'ajout_sel', 'regime_special'
]

# Appliquer le LabelEncoder à chaque colonne catégorielle
for col in categorical_columns:
    df_imputed[col] = label_encoder.fit_transform(df_imputed[col].astype(str))

 #*******************************************Standardisation des données******************************************
    from sklearn.preprocessing import StandardScaler

    # Initialisation du scaler
    scaler = StandardScaler()

    # Appliquer la transformation de standardisation sur les colonnes spécifiées
    df_imputed[['heur_trav', 'bmi', 'taille', 'Ntop', 'Npop', 'prev', 'pm10', 'pm2_5', 'carbon_monoxide',
                'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'grass_pollen', 'temps_act_phy', 'p_animal',
                'p_vegetale', 'gras_animal',
                'vistes_medecins', 'fumeur', 'sedentaire', 'achats_distributeurs',
                'poids_moyen']] = scaler.fit_transform(
        df_imputed[['heur_trav', 'bmi', 'taille', 'Ntop', 'Npop', 'prev', 'pm10', 'pm2_5', 'carbon_monoxide',
                    'nitrogen_dioxide', 'sulphur_dioxide', 'ozone', 'grass_pollen', 'temps_act_phy', 'p_animal',
                    'p_vegetale', 'gras_animal',
                    'vistes_medecins', 'fumeur', 'sedentaire', 'achats_distributeurs', 'poids_moyen']])

print(df_imputed.head())