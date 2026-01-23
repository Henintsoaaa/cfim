# app/main.py
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.schemas import PredictionInput, PredictionOutput
from app.predict import make_prediction
from app.model import FEATURE_NAMES
from app.bulletin_parser import bulletin_parser, parse_and_prepare
from app.user_input_parser import user_input_parser

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

@app.post("/predict-bulletin")
def predict_from_bulletin(
    request: Request,
    bulletin_text: str = Form(...)
):
    """Endpoint pour analyser un bulletin météo maritime"""
    # Parser le bulletin
    parsed_data, model_input_tuple = parse_and_prepare(bulletin_text)
    
    # Extraire les valeurs du tuple
    (vent_vitesse, hauteur_mer, etat_mer, visibilite, 
     jour, mois, annee, latitude, longitude) = model_input_tuple
    
    # Faire la prédiction
    pred, proba = make_prediction(
        vent_vitesse, hauteur_mer, etat_mer, visibilite,
        jour, mois, annee, latitude, longitude
    )
    
    # Préparer model_input dict pour affichage
    model_input = {
        'vent_vitesse': vent_vitesse,
        'hauteur_mer': hauteur_mer,
        'etat_mer': etat_mer,
        'visibilite': visibilite,
        'jour': jour,
        'mois': mois,
        'annee': annee,
        'latitude': latitude,
        'longitude': longitude
    }
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "features": FEATURE_NAMES,
            "prediction": pred,
            "probability": proba,
            "parsed_data": parsed_data,
            "model_input": model_input,
            "bulletin_text": bulletin_text
        }
    )

@app.post("/predict-simple")
def predict_from_simple_input(
    request: Request,
    date_obs: str = Form(...),
    lieu: str = Form(...),
    vent_desc: str = Form(...),
    etat_mer_desc: str = Form(...),
    temps_desc: str = Form(...)
):
    """Endpoint pour saisie simplifiée (descriptions naturelles)"""
    # Parser les inputs utilisateur
    parsed_input = user_input_parser.parse_user_input(
        date_input=date_obs,
        vent_input=vent_desc,
        etat_mer_input=etat_mer_desc,
        temps_input=temps_desc,
        lieu_input=lieu
    )
    
    # Faire la prédiction
    pred, proba = make_prediction(
        parsed_input['vent_vitesse'],
        parsed_input['hauteur_mer'],
        parsed_input['etat_mer'],
        parsed_input['visibilite'],
        parsed_input['jour'],
        parsed_input['mois'],
        parsed_input['annee'],
        parsed_input['latitude'],
        parsed_input['longitude']
    )
    
    # Préparer model_input pour affichage
    model_input = {
        'vent_vitesse': parsed_input['vent_vitesse'],
        'hauteur_mer': parsed_input['hauteur_mer'],
        'etat_mer': parsed_input['etat_mer'],
        'visibilite': parsed_input['visibilite'],
        'jour': parsed_input['jour'],
        'mois': parsed_input['mois'],
        'annee': parsed_input['annee'],
        'latitude': parsed_input['latitude'],
        'longitude': parsed_input['longitude']
    }
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "features": FEATURE_NAMES,
            "prediction": pred,
            "probability": proba,
            "model_input": model_input,
            "parsed_info": parsed_input.get('parsed_info')
        }
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)