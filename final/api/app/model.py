# app/model.py
import joblib

MODEL_PATH = "best_model_xgb_weighted.joblib"
FEATURES_PATH = "model_features_info.joblib"

model_data = joblib.load(MODEL_PATH)
features_info = joblib.load(FEATURES_PATH)

# Extraire le modèle, le scaler et les features
model = model_data["model"]
scaler = model_data["scaler"]
feature_cols = model_data["feature_cols"]
threshold = model_data.get("threshold", 0.5)

FEATURE_NAMES = features_info["feature_columns"]
