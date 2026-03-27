import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.auth import authenticate, create_token
from app.database import add_history, get_history
from app.predict import predict_risk
from app.predict_heart import predict_heart
from app.predict_router import predict

app = FastAPI(title="Healthcare Risk Prediction API")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.models import (
    HeartRequest,
    LoginRequest,
    MultiDiseaseRequest,
    PredictRequest,
    PredictionResponse,
    TokenResponse,
)


@app.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    token = create_token(req.userId)
    return {"token": token}


@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(
    req: MultiDiseaseRequest,
    user_id: str = Depends(authenticate),
):
    try:
        result = predict({"disease": req.disease, **req.data})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc

    add_history(user_id, {"disease": req.disease, "input": req.data, "result": result})
    return result


@app.post("/predict-risk", response_model=PredictionResponse)
def predict_risk_endpoint(
    req: PredictRequest,
    user_id: str = Depends(authenticate)
):
    data = req.model_dump()
    try:
        result = predict_risk(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc

    add_history(user_id, {"disease": "diabetes", "input": data, "result": result})

    return result


@app.post("/predict-heart", response_model=PredictionResponse)
def predict_heart_endpoint(
    req: HeartRequest,
    user_id: str = Depends(authenticate),
):
    data = req.model_dump()
    try:
        result = predict_heart(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Prediction failed") from exc

    add_history(user_id, {"disease": "heart", "input": data, "result": result})
    return result


@app.get("/patient-history")
def history(user_id: str = Depends(authenticate)):
    return get_history(user_id)
