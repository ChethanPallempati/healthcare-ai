import joblib
import os

import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, "heart_model.pkl"))
encoders = joblib.load(os.path.join(BASE_DIR, "heart_encoders.pkl"))
FEATURES = joblib.load(os.path.join(BASE_DIR, "heart_features.pkl"))


def predict_heart(data):
    df = pd.DataFrame([data])

    for col in df.columns:
        if col in encoders:
            df[col] = df[col].astype(str).str.strip().str.title()

            le = encoders[col]

            df[col] = df[col].apply(
                lambda x: x if x in le.classes_ else le.classes_[0]
            )

            df[col] = le.transform(df[col])

    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    for col in FEATURES:
        if col not in df:
            df[col] = 0

    df = df[FEATURES]

    prediction = model.predict(df)[0]
    probability = float(model.predict_proba(df)[0][1])

    if probability < 0.4:
        risk = "Low"
    elif probability < 0.7:
        risk = "Medium"
    else:
        risk = "High"

    top_factors = []
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feature_importance = sorted(
            zip(FEATURES, importances),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        top_factors = [f[0] for f in feature_importance]

    recommendations = []
    if data.get("Smoking", "").strip().lower() == "yes":
        recommendations.append("Smoking increases cardiovascular risk: discuss a cessation plan.")
    if int(data.get("Systolic", 0)) >= 140 or int(data.get("Diastolic", 0)) >= 90:
        recommendations.append("Blood pressure is elevated: follow up with a clinician.")
    if int(data.get("Cholesterol_level_mg_dL", 0)) >= 200:
        recommendations.append("High cholesterol may need dietary changes and medical review.")
    if not recommendations:
        recommendations.append("Continue heart-healthy habits and routine preventive care.")

    return {
        "disease": "Heart Disease",
        "prediction": int(prediction),
        "risk": risk,
        "probability": round(float(probability), 2),
        "topFactors": top_factors,
        "recommendations": recommendations,
    }
