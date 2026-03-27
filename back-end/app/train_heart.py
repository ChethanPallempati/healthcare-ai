import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "heart.csv")
MODEL_PATH = os.path.join(BASE_DIR, "heart_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "heart_encoders.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "heart_features.pkl")

df = pd.read_csv(DATA_PATH)

df = df.drop(["Name", "Medications", "Treatment"], axis=1)

label_encoders = {}
for col in df.columns:
    if df[col].dtype == "object":
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

X = df.drop("Diagnosis", axis=1)
y = df["Diagnosis"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

joblib.dump(model, MODEL_PATH)
joblib.dump(label_encoders, ENCODER_PATH)
joblib.dump(X.columns.tolist(), FEATURES_PATH)

print(f"Saved model to {MODEL_PATH}")
print(f"Saved encoders to {ENCODER_PATH}")
print(f"Saved feature list to {FEATURES_PATH}")
