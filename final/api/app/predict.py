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
    Fait une prédiction à partir des inputs du formulaire
    AVEC RÈGLES MÉTIER pour conditions extrêmes
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
    
    # RÈGLES MÉTIER: Détecter automatiquement les conditions extrêmes
    # Ces seuils sont basés sur les standards maritimes
    conditions_extremes = (
        vent_vitesse > 20 or  # Vent fort
        hauteur_mer > 6 or    # Mer très grosse
        etat_mer >= 7 or      # État mer dangereux
        visibilite < 3        # Visibilité très réduite
    )
    
    # Conditions CRITIQUES (risque immédiat)
    conditions_critiques = (
        vent_vitesse > 25 or
        hauteur_mer > 8 or
        etat_mer >= 8 or
        visibilite < 2
    )
    
    # Si conditions critiques, forcer la détection
    if conditions_critiques:
        return 1, 0.95  # 95% de risque
    
    # Créer toutes les features nécessaires (retourne déjà un DataFrame)
    features_df = create_features_from_input(
        vent_vitesse, hauteur_mer, etat_mer, visibilite,
        jour, mois, annee, latitude, longitude
    )
    
    # Sélectionner l'ordre correct des colonnes
    X = features_df[feature_cols]
    
    # Appliquer le scaler
    X_scaled = scaler.transform(X)
    
    # Prédire la probabilité
    proba = model.predict_proba(X_scaled)[0][1]  # Probabilité de la classe positive (risque)
    
    # Si conditions extrêmes, augmenter la probabilité
    if conditions_extremes:
        proba = max(proba, 0.70)  # Minimum 70% pour conditions extrêmes
    
    # Appliquer le threshold optimisé
    prediction = 1 if proba >= threshold else 0

    return prediction, proba
