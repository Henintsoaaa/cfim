# app/predict.py
import numpy as np
import pandas as pd
from app.model import model, scaler, feature_cols, threshold

def make_prediction(
    vent_vitesse: float,
    hauteur_mer: float,
    etat_mer: float,
    visibilite: float,
    jour: int,
    mois: int,
    annee: int,
    latitude: float,
    longitude: float
):
    """
    Fait une prédiction à partir des inputs du formulaire.
    
    Approche hybride:
    1. Le modèle ML prédit sur les données plafonnées (dans sa distribution)
    2. Pour les conditions HORS distribution (extrêmes), on ajuste la probabilité
       proportionnellement à l'écart par rapport aux limites du dataset
    
    Cela permet au modèle de fonctionner correctement tout en gérant
    les conditions extrêmes qu'il n'a jamais vues pendant l'entraînement.
    """
    from app.feature_engineering import create_features_from_input
    
    # Gérer les valeurs None avec des valeurs par défaut
    vent_vitesse = vent_vitesse if vent_vitesse is not None else 0
    hauteur_mer = hauteur_mer if hauteur_mer is not None else 0
    etat_mer = etat_mer if etat_mer is not None else 0
    visibilite = visibilite if visibilite is not None else 5
    jour = jour if jour is not None else 1
    mois = mois if mois is not None else 1
    annee = annee if annee is not None else 2020
    latitude = latitude if latitude is not None else -18.0
    longitude = longitude if longitude is not None else 47.0
    
    # Créer toutes les features nécessaires (retourne un DataFrame)
    features_df = create_features_from_input(
        vent_vitesse, hauteur_mer, etat_mer, visibilite,
        jour, mois, annee, latitude, longitude
    )
    
    # Extraire le score "hors distribution" AVANT de sélectionner les colonnes du modèle
    score_hors_distrib = 0.0
    if '_score_hors_distribution' in features_df.columns:
        score_hors_distrib = features_df['_score_hors_distribution'].values[0]
    
    # Sélectionner l'ordre correct des colonnes pour le modèle
    X = features_df[feature_cols]
    
    # Appliquer le scaler
    X_scaled = scaler.transform(X)
    
    # Prédire la probabilité avec le modèle ML
    proba_model = model.predict_proba(X_scaled)[0][1]
    
    # AJUSTEMENT HYBRIDE pour conditions hors distribution
    # Le score_hors_distrib augmente quand les valeurs dépassent les limites du dataset
    # On l'utilise pour booster la probabilité de manière proportionnelle
    if score_hors_distrib > 0:
        # Formule: proba_finale = proba_model + (1 - proba_model) * boost
        # Où boost augmente progressivement avec les conditions extrêmes
        boost = min(score_hors_distrib, 1.5) * 0.6  # Boost plus fort
        proba = proba_model + (1 - proba_model) * boost
    else:
        proba = proba_model
    
    # S'assurer que la proba reste dans [0, 1]
    proba = max(0.0, min(1.0, proba))
    
    # Appliquer le threshold optimisé (calculé pendant l'entraînement)
    prediction = 1 if proba >= threshold else 0

    return prediction, proba
