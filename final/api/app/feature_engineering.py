# app/feature_engineering.py
import numpy as np
import pandas as pd
from datetime import datetime

def create_features_from_input(
    vent_vitesse: float,
    hauteur_mer: float,
    etat_mer: float,
    visibilite: float,
    jour: int,
    mois: int,
    annee: int,
    latitude: float,
    longitude: float
) -> dict:
    """
    Crée toutes les features nécessaires au modèle à partir des inputs du formulaire
    """
    # Date et temps
    date = datetime(annee, mois, jour)
    jour_annee = date.timetuple().tm_yday
    jour_semaine = date.weekday()
    trimestre = (mois - 1) // 3 + 1
    
    # Features cycliques pour le temps
    jour_annee_sin = np.sin(2 * np.pi * jour_annee / 365.25)
    jour_annee_cos = np.cos(2 * np.pi * jour_annee / 365.25)
    jour_semaine_sin = np.sin(2 * np.pi * jour_semaine / 7)
    mois_sin = np.sin(2 * np.pi * mois / 12)
    mois_cos = np.cos(2 * np.pi * mois / 12)
    
    # Saison cyclonique (novembre-avril pour l'océan Indien)
    saison_cyclonique = 1 if mois in [11, 12, 1, 2, 3, 4] else 0
    
    # Mois à haut risque
    mois_haut_risque = 1 if mois in [1, 2, 3, 12] else 0
    
    # Features de vent
    vent_moyen = vent_vitesse
    vent_vitesse_max = vent_vitesse * 1.2  # Estimation
    vent_vitesse_min = vent_vitesse * 0.8  # Estimation
    vent_cv = 0.15  # Coefficient de variation par défaut
    vent_direction_deg = 0.0  # Par défaut
    
    # Features lag (valeurs précédentes non disponibles, on utilise les valeurs actuelles)
    vent_moyen_lag1 = vent_moyen
    vent_vitesse_max_lag1 = vent_vitesse_max
    
    # Features de mer
    mer_hauteur_min = hauteur_mer * 0.8
    mer_score_min = etat_mer * 0.8
    mer_score_variabilite = 0.1  # Par défaut
    
    # Features météo
    temps_nuageux = 1 if visibilite < 5 else 0
    temps_precipitation = 1 if visibilite < 2 else 0
    vent_precipitation = vent_vitesse * temps_precipitation
    
    # Scores de danger
    # Score basé sur vent, mer et visibilité
    score_vent = min(vent_vitesse / 50, 1.0)  # Normaliser à 0-1
    score_mer = min(hauteur_mer / 10, 1.0)
    score_visibilite = max(1 - visibilite / 10, 0)
    
    temps_score_danger = (score_vent + score_mer + score_visibilite) / 3
    score_danger_composite = temps_score_danger
    
    # Score saisonnier
    score_saison = saison_cyclonique * 0.5 + mois_haut_risque * 0.5
    
    # Nombre de conditions défavorables
    nb_conditions = sum([
        vent_vitesse > 30,  # Vent fort
        hauteur_mer > 4,     # Mer agitée
        etat_mer > 3,        # État mer défavorable
        visibilite < 5       # Faible visibilité
    ])
    
    nb_conditions_defavorables = nb_conditions
    nb_conditions_defavorables_lag1 = nb_conditions  # Pas d'historique
    nb_conditions_defavorables_lag2 = nb_conditions
    nb_conditions_defavorables_rolling3 = nb_conditions
    
    # Créer le dictionnaire avec toutes les features dans l'ordre attendu
    features = {
        'vent_cv': vent_cv,
        'nb_conditions_defavorables_lag2': nb_conditions_defavorables_lag2,
        'jour_annee': jour_annee,
        'temps_nuageux': temps_nuageux,
        'annee': annee,
        'temps_precipitation': temps_precipitation,
        'temps_score_danger': temps_score_danger,
        'vent_moyen_lag1': vent_moyen_lag1,
        'trimestre': trimestre,
        'vent_direction_deg': vent_direction_deg,
        'jour_annee_sin': jour_annee_sin,
        'nb_conditions_defavorables_lag1': nb_conditions_defavorables_lag1,
        'nb_conditions_defavorables': nb_conditions_defavorables,
        'mer_score_min': mer_score_min,
        'jour': jour,
        'mois_haut_risque': mois_haut_risque,
        'nb_conditions_defavorables_rolling3': nb_conditions_defavorables_rolling3,
        'jour_semaine_sin': jour_semaine_sin,
        'jour_semaine': jour_semaine,
        'mois_cos': mois_cos,
        'vent_vitesse_max_lag1': vent_vitesse_max_lag1,
        'mois_sin': mois_sin,
        'mois': mois,
        'mer_score_variabilite': mer_score_variabilite,
        'score_danger_composite': score_danger_composite,
        'vent_vitesse_min': vent_vitesse_min,
        'saison_cyclonique': saison_cyclonique,
        'vent_precipitation': vent_precipitation,
        'jour_annee_cos': jour_annee_cos,
        'score_saison': score_saison,
        'mer_hauteur_min': mer_hauteur_min,
        'vent_vitesse_max': vent_vitesse_max,
        'vent_moyen': vent_moyen
    }
    
    return features
