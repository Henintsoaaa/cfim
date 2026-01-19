# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.schemas import PredictionInput, PredictionOutput
from app.predict import make_prediction
from app.model import FEATURE_NAMES

app = FastAPI(title="ML Model API")

templates = Jinja2Templates(directory="app/templates")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# ========== ENDPOINTS ICI ==========

@app.post("/predict", response_model=PredictionOutput)
def predict_api(data: PredictionInput):
    """Endpoint API pour prédictions (JSON)"""
    if len(data.features) != 9:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Exactement 9 features requises")
    
    pred, proba = make_prediction(
        data.features[0],  # vent_vitesse
        data.features[1],  # hauteur_mer
        data.features[2],  # etat_mer
        data.features[3],  # visibilite
        int(data.features[4]),  # jour
        int(data.features[5]),  # mois
        int(data.features[6]),  # annee
        data.features[7],  # latitude
        data.features[8]   # longitude
    )
    return {"prediction": int(pred), "probability": float(proba)}

@app.get("/")
def home(request: Request):
    """Page d'accueil avec formulaire"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "features": FEATURE_NAMES}
    )

@app.post("/predict-ui")
def predict_ui(
    request: Request,
    vent_vitesse: float = Form(...),
    hauteur_mer: float = Form(...),
    etat_mer: float = Form(...),
    visibilite: float = Form(...),
    jour: int = Form(...),
    mois: int = Form(...),
    annee: int = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...)
):
    """Endpoint pour soumission formulaire HTML"""
    pred, proba = make_prediction(
        vent_vitesse, hauteur_mer, etat_mer, visibilite,
        jour, mois, annee, latitude, longitude
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "features": FEATURE_NAMES,
            "prediction": pred,
            "probability": proba
        }
    )