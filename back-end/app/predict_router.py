from app.predict_heart import predict_heart
from app.predict import predict_risk


def predict(data):
    disease = data.get("disease")

    if disease == "heart":
        return predict_heart(data)
    if disease == "diabetes":
        return predict_risk(data)

    raise ValueError("Invalid disease type")
