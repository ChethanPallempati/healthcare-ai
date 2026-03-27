from typing import List, Optional

from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: int

class PredictionResponse(BaseModel):
    disease: str
    risk: str
    probability: float
    topFactors: List[str]
    recommendations: List[str]
    prediction: Optional[int] = None

class LoginRequest(BaseModel):
    userId: str

class TokenResponse(BaseModel):
    token: str


class HeartRequest(BaseModel):
    Gender: str
    Age: int
    Chest_pain: str
    Shortness_of_breath: str
    Fatigue: str
    Systolic: int
    Diastolic: int
    Heart_rate_bpm: int
    Cholesterol_level_mg_dL: int
    Diabetes: str
    Hypertension: str
    Smoking: str
    Obesity: str


class MultiDiseaseRequest(BaseModel):
    disease: str = Field(..., pattern="^(heart|diabetes)$")
    data: dict
