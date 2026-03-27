import argparse
import os

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

columns = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age", "outcome"
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_PATH = os.path.join(BASE_DIR, "back-end", "app", "model.pkl")


def parse_args():
    parser = argparse.ArgumentParser(description="Train the diabetes risk model from a local CSV file.")
    parser.add_argument("--data", required=True, help="Path to a local CSV file in the Pima-style 9-column format.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH, help="Where to write the trained model pickle.")
    return parser.parse_args()


def main():
    args = parse_args()

    data_frame = pd.read_csv(args.data, names=columns)
    X = data_frame.drop("outcome", axis=1)
    y = data_frame["outcome"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    importance = model.feature_importances_
    for index, column in enumerate(X.columns):
        print(f"{column}: {importance[index]:.4f}")

    joblib.dump(model, args.output)
    print(f"Model saved to {args.output}")


if __name__ == "__main__":
    main()
