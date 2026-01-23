# app/model.py
import joblib
import os

# Chemins absolus vers les modèles (dans le dossier parent de app/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "best_model_xgb_weighted.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "model_features_info.joblib")

model_data = joblib.load(MODEL_PATH)
features_info = joblib.load(FEATURES_PATH)

# Extraire le modèle, le scaler et les features
model = model_data["model"]
scaler = model_data["scaler"]
feature_cols = model_data["feature_cols"]
threshold = model_data.get("threshold", 0.5)

FEATURE_NAMES = features_info["feature_columns"]
