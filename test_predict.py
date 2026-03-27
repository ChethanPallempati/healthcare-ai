import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "back-end"))

from app.predict import predict_risk

sample = {
    "pregnancies": 2,
    "glucose": 160,
    "blood_pressure": 70,
    "skin_thickness": 20,
    "insulin": 80,
    "bmi": 32,
    "diabetes_pedigree": 0.5,
    "age": 55
}

result = predict_risk(sample)

print(result)
