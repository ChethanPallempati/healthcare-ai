import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

import app.main as main_module
from app.database import PATIENT_HISTORY


client = TestClient(main_module.app)


def auth_headers(user_id="demo-user"):
    token = client.post("/login", json={"userId": user_id}).json()["token"]
    return {"Authorization": f"Bearer {token}"}


def setup_function():
    PATIENT_HISTORY.clear()


def test_predict_risk_requires_auth():
    response = client.post(
        "/predict-risk",
        json={
            "pregnancies": 1,
            "glucose": 120,
            "blood_pressure": 70,
            "skin_thickness": 20,
            "insulin": 80,
            "bmi": 28,
            "diabetes_pedigree": 0.4,
            "age": 35,
        },
    )

    assert response.status_code == 401


def test_predict_risk_returns_normalized_response_and_history(monkeypatch):
    def fake_predict(data):
        return {
            "disease": "Diabetes",
            "prediction": 1,
            "risk": "Medium",
            "probability": 0.61,
            "topFactors": ["glucose", "bmi", "age"],
            "recommendations": ["Schedule routine follow-up."],
        }

    monkeypatch.setattr(main_module, "predict_risk", fake_predict)

    response = client.post(
        "/predict-risk",
        headers=auth_headers(),
        json={
            "pregnancies": 2,
            "glucose": 160,
            "blood_pressure": 70,
            "skin_thickness": 20,
            "insulin": 80,
            "bmi": 32,
            "diabetes_pedigree": 0.5,
            "age": 55,
        },
    )

    assert response.status_code == 200
    assert response.json()["risk"] == "Medium"

    history = client.get("/patient-history", headers=auth_headers()).json()
    assert len(history) == 1
    assert history[0]["disease"] == "diabetes"
    assert history[0]["result"]["disease"] == "Diabetes"


def test_predict_heart_requires_auth_and_records_history(monkeypatch):
    def fake_predict(data):
        return {
            "disease": "Heart Disease",
            "prediction": 0,
            "risk": "Low",
            "probability": 0.22,
            "topFactors": ["Smoking", "Systolic", "Cholesterol_level_mg_dL"],
            "recommendations": ["Continue preventive care."],
        }

    monkeypatch.setattr(main_module, "predict_heart", fake_predict)
    headers = auth_headers("heart-user")

    response = client.post(
        "/predict-heart",
        headers=headers,
        json={
            "Gender": "Male",
            "Age": 40,
            "Chest_pain": "No",
            "Shortness_of_breath": "No",
            "Fatigue": "No",
            "Systolic": 120,
            "Diastolic": 80,
            "Heart_rate_bpm": 70,
            "Cholesterol_level_mg_dL": 180,
            "Diabetes": "No",
            "Hypertension": "No",
            "Smoking": "No",
            "Obesity": "No",
        },
    )

    assert response.status_code == 200
    assert response.json()["disease"] == "Heart Disease"

    history = client.get("/patient-history", headers=headers).json()
    assert len(history) == 1
    assert history[0]["disease"] == "heart"


def test_predict_endpoint_rejects_unknown_disease():
    response = client.post(
        "/predict",
        headers=auth_headers(),
        json={"disease": "unknown", "data": {}},
    )

    assert response.status_code == 422
