import joblib
import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")
model = joblib.load(model_path)

FEATURES = [
    "pregnancies", "glucose", "blood_pressure",
    "skin_thickness", "insulin", "bmi",
    "diabetes_pedigree", "age"
]


def predict_risk(data: dict):
    input_df = pd.DataFrame([[data.get(feature, 0) for feature in FEATURES]], columns=FEATURES)

    prediction = int(model.predict(input_df)[0])
    probability = float(model.predict_proba(input_df)[0][1])

    if probability < 0.3:
        risk = "Low"
    elif probability < 0.7:
        risk = "Medium"
    else:
        risk = "High"

    importances = getattr(model, "feature_importances_", [0] * len(FEATURES))
    factor_scores = dict(zip(FEATURES, importances))
    top_factors = sorted(factor_scores, key=factor_scores.get, reverse=True)[:3]

    recommendations = []
    if data.get("glucose", 0) > 140:
        recommendations.append("High glucose: monitor diet and blood sugar levels.")
    if data.get("bmi", 0) > 30:
        recommendations.append("High BMI: follow a weight management plan.")
    if data.get("age", 0) > 50:
        recommendations.append("Age over 50: schedule regular medical checkups.")
    if not recommendations:
        recommendations.append("Maintain regular exercise, balanced nutrition, and routine screenings.")

    return {
        "disease": "Diabetes",
        "prediction": prediction,
        "risk": risk,
        "probability": round(probability, 2),
        "topFactors": top_factors,
        "recommendations": recommendations,
    }
