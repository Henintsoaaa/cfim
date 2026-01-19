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
    """
    from app.feature_engineering import create_features_from_input
    
    # Créer toutes les features nécessaires
    features_dict = create_features_from_input(
        vent_vitesse, hauteur_mer, etat_mer, visibilite,
        jour, mois, annee, latitude, longitude
    )
    
    # Convertir en DataFrame avec l'ordre correct des colonnes
    X = pd.DataFrame([features_dict])[feature_cols]
    
    # Appliquer le scaler
    X_scaled = scaler.transform(X)
    
    # Prédire la probabilité
    proba = model.predict_proba(X_scaled)[0][1]  # Probabilité de la classe positive (risque)
    
    # Appliquer le threshold optimisé
    prediction = 1 if proba >= threshold else 0

    return prediction, proba
