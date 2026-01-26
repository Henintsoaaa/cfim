# app/feature_engineering.py
import numpy as np
import pandas as pd
from datetime import datetime

def engineer_features_from_base(base_df: pd.DataFrame) -> pd.DataFrame:
    """
    Feature engineering avancé - adapté du notebook model_final.ipynb
    Prend un DataFrame avec les features de base du dataset et génère toutes les features nécessaires
    """
    df = base_df.copy()
    
    # 1. INTERACTIONS MULTIPLICATIVES (conditions combinées dangereuses)
    df['vent_x_mer'] = df['vent_vitesse_max'] * df['mer_hauteur_max']
    df['vent_x_score_mer'] = df['vent_vitesse_max'] * df['mer_score_max']
    df['mer_x_danger'] = df['mer_hauteur_max'] * df['temps_score_danger']
    df['vent_x_danger'] = df['vent_vitesse_max'] * df['temps_score_danger']
    
    # 2. SCORES COMPOSITES (indices de danger)
    df['indice_danger_global'] = (
        0.35 * (df['vent_vitesse_max'] / 30) +
        0.35 * (df['mer_hauteur_max'] / 5) +
        0.30 * df['temps_score_danger']
    )
    
    df['indice_mer_extreme'] = df['mer_hauteur_max'] ** 2 * df['mer_score_max']
    df['indice_vent_extreme'] = df['vent_vitesse_max'] ** 1.5 * (df['vent_rafales'] / (df['vent_vitesse_min'] + 1))
    
    # 3. RATIOS ET AMPLITUDES
    df['ratio_vent_rafales'] = df['vent_rafales'] / (df['vent_vitesse_max'] + 1)
    df['amplitude_vent_pct'] = df['vent_amplitude'] / (df['vent_moyen'] + 1)
    df['ratio_mer_hauteur'] = df['mer_hauteur_max'] / (df['mer_hauteur_min'] + 0.1)
    
    # 4. INDICATEURS BOOLÉENS (seuils critiques)
    df['vent_critique'] = (df['vent_vitesse_max'] > 20).astype(int)
    df['mer_critique'] = (df['mer_hauteur_max'] > 4).astype(int)
    df['visibilite_critique'] = (df['temps_score_danger'] > 0.6).astype(int)
    df['conditions_multiples_critiques'] = df['vent_critique'] + df['mer_critique'] + df['visibilite_critique']
    
    # 5. FEATURES TEMPORELLES AMÉLIORÉES
    df['saison_cyclonique_intensite'] = df['mois'].map({
        11: 0.5, 12: 0.8, 1: 1.0, 2: 1.0, 3: 0.9, 4: 0.6
    }).fillna(0.0)
    
    df['danger_saisonnier'] = df['saison_cyclonique_intensite'] * df['indice_danger_global']
    
    # 6. FEATURES LAG AMÉLIORÉES (si disponibles)
    if 'score_risque_lag1' in df.columns and 'score_risque' in df.columns:
        df['acceleration_risque'] = df['score_risque'] - df['score_risque_lag1']
        df['persistance_risque'] = ((df['score_risque'] > 5) & (df['score_risque_lag1'] > 5)).astype(int)
    
    return df


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
    ADAPTÉ pour correspondre au nouveau modèle avec feature engineering avancé
    """
    # Date et temps
    date = datetime(annee, mois, jour)
    jour_annee = date.timetuple().tm_yday
    jour_semaine = date.weekday()
    
    # Features cycliques
    jour_annee_sin = np.sin(2 * np.pi * jour_annee / 365.25)
    jour_annee_cos = np.cos(2 * np.pi * jour_annee / 365.25)
    jour_semaine_sin = np.sin(2 * np.pi * jour_semaine / 7)
    mois_sin = np.sin(2 * np.pi * mois / 12)
    mois_cos = np.cos(2 * np.pi * mois / 12)
    
    # Saison cyclonique
    saison_cyclonique = 1 if mois in [11, 12, 1, 2, 3, 4] else 0
    weekend = 1 if jour_semaine >= 5 else 0
    
    # PLAFONNEMENT CRITIQUE: Limiter aux valeurs max du dataset d'entraînement
    # Dataset max: vent=25 km/h, mer=9m
    # NOTE: On garde les vraies valeurs pour le calcul du score de danger
    #       mais on plafonne pour les features du modèle ML
    vent_vitesse_pour_model = min(vent_vitesse, 25.0)
    hauteur_mer_pour_model = min(hauteur_mer, 9.0)
    etat_mer_capped = min(etat_mer, 9.0)
    
    # Calculer le score "hors distribution" pour conditions dangereuses
    # Basé sur les standards maritimes internationaux:
    # - Vent > 20 km/h = mer peu agitée (brise fraîche)
    # - Vent > 25 km/h = mer agitée (coup de vent)
    # - Mer > 2.5m = mer agitée
    # - Mer > 4m = mer forte à très forte
    # - Visibilité < 5 = conditions dégradées
    # - Visibilité < 3 = conditions dangereuses
    
    score_hors_distribution = 0.0
    
    # Vent - seuils abaissés
    if vent_vitesse > 20:
        score_hors_distribution += (vent_vitesse - 20) / 15  # +0.067 par km/h au-dessus de 20
    
    # Hauteur mer - seuils abaissés
    if hauteur_mer > 2.5:
        score_hors_distribution += (hauteur_mer - 2.5) / 4  # +0.25 par mètre au-dessus de 2.5
    
    # État mer
    if etat_mer > 5:
        score_hors_distribution += (etat_mer - 5) / 4  # +0.25 par point au-dessus de 5
    
    # Visibilité - seuil relevé
    if visibilite < 5:
        score_hors_distribution += (5 - visibilite) / 5  # +0.2 par point en dessous de 5
    
    # FEATURES DE BASE (identiques au dataset d'entraînement)
    vent_vitesse_min = vent_vitesse_pour_model * 0.8
    vent_vitesse_max = min(vent_vitesse_pour_model * 1.2, 25.0)
    vent_rafales = min(vent_vitesse_max * 1.15, 25.0)
    vent_direction_deg = 0.0
    
    mer_score_min = max(0, etat_mer_capped - 1)
    mer_score_max = etat_mer_capped
    mer_hauteur_min = hauteur_mer_pour_model * 0.7
    mer_hauteur_max = min(hauteur_mer_pour_model, 9.0)
    
    # Conditions météo (convertir visibilite 0-10 vers scores binaires)
    temps_precipitation = 1 if visibilite < 5 else 0
    temps_orage = 1 if visibilite < 3 else 0
    temps_visibilite_reduite = 1 if visibilite < 6 else 0
    temps_clair = 1 if visibilite >= 8 else 0
    temps_nuageux = 1 if 4 <= visibilite < 8 else 0
    temps_score_danger = max(0, 1 - visibilite / 10)
    
    score_risque = (
        0.3 * (vent_vitesse_max / 30) +
        0.3 * (mer_hauteur_max / 6) +
        0.2 * (mer_score_max / 9) +
        0.2 * temps_score_danger
    ) * 10
    
    # Features dérivées
    vent_amplitude = vent_vitesse_max - vent_vitesse_min
    vent_moyen = (vent_vitesse_max + vent_vitesse_min) / 2
    mer_amplitude = mer_hauteur_max - mer_hauteur_min
    mer_moyenne = (mer_hauteur_max + mer_hauteur_min) / 2
    
    # Indicateurs booléens
    vent_fort = 1 if vent_vitesse_max > 20 else 0
    vent_violent = 1 if vent_vitesse_max > 25 else 0
    rafales_fortes = 1 if vent_rafales > 30 else 0
    mer_agitee = 1 if mer_hauteur_max > 2 else 0
    mer_forte = 1 if mer_hauteur_max > 4 else 0
    
    # Features lag (valeurs par défaut car pas d'historique)
    vent_vitesse_max_lag1 = vent_vitesse_max
    vent_vitesse_max_trend = 0
    mer_hauteur_max_lag1 = mer_hauteur_max
    mer_hauteur_max_trend = 0
    score_risque_lag1 = score_risque
    score_risque_trend = 0
    vent_moyen_lag1 = vent_moyen
    vent_moyen_trend = 0
    
    # Créer le dictionnaire de base
    base_features = {
        'vent_vitesse_min': vent_vitesse_min,
        'vent_vitesse_max': vent_vitesse_max,
        'vent_rafales': vent_rafales,
        'vent_direction_deg': vent_direction_deg,
        'mer_score_min': mer_score_min,
        'mer_score_max': mer_score_max,
        'mer_hauteur_min': mer_hauteur_min,
        'mer_hauteur_max': mer_hauteur_max,
        'temps_precipitation': temps_precipitation,
        'temps_orage': temps_orage,
        'temps_visibilite_reduite': temps_visibilite_reduite,
        'temps_clair': temps_clair,
        'temps_nuageux': temps_nuageux,
        'temps_score_danger': temps_score_danger,
        'score_risque': score_risque,
        'annee': annee,
        'mois': mois,
        'jour': jour,
        'jour_semaine': jour_semaine,
        'jour_annee': jour_annee,
        'saison_cyclonique': saison_cyclonique,
        'weekend': weekend,
        'mois_sin': mois_sin,
        'mois_cos': mois_cos,
        'jour_annee_sin': jour_annee_sin,
        'jour_annee_cos': jour_annee_cos,
        'vent_amplitude': vent_amplitude,
        'vent_moyen': vent_moyen,
        'mer_amplitude': mer_amplitude,
        'mer_moyenne': mer_moyenne,
        'vent_fort': vent_fort,
        'vent_violent': vent_violent,
        'rafales_fortes': rafales_fortes,
        'mer_agitee': mer_agitee,
        'mer_forte': mer_forte,
        'vent_vitesse_max_lag1': vent_vitesse_max_lag1,
        'vent_vitesse_max_trend': vent_vitesse_max_trend,
        'mer_hauteur_max_lag1': mer_hauteur_max_lag1,
        'mer_hauteur_max_trend': mer_hauteur_max_trend,
        'score_risque_lag1': score_risque_lag1,
        'score_risque_trend': score_risque_trend,
        'vent_moyen_lag1': vent_moyen_lag1,
        'vent_moyen_trend': vent_moyen_trend,
        # Score spécial pour conditions hors distribution
        '_score_hors_distribution': score_hors_distribution
    }
    
    # Créer DataFrame avec les features de base
    base_df = pd.DataFrame([base_features])
    
    # Appliquer le feature engineering avancé (retourne DataFrame avec une ligne)
    engineered_df = engineer_features_from_base(base_df)
    
    # Charger la liste des colonnes attendues par le modèle
    import joblib
    import os
    try:
        # Chemin absolu vers le modèle
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'best_model_xgb_weighted.joblib')
        model_data = joblib.load(model_path)
        expected_cols = model_data['feature_cols']
        
        # Ajouter toutes les colonnes manquantes avec valeur 0
        for col in expected_cols:
            if col not in engineered_df.columns:
                engineered_df[col] = 0
                
    except Exception as e:
        print(f"Warning: Could not load model features: {e}")
    
    # Retourner DataFrame (pas dict!)
    return engineered_df
