# Healthcare AI

This repository contains:
A full-stack healthcare risk prediction demo built with FastAPI, React, and scikit-learn. The app lets a user log in, submit diabetes or heart-disease risk inputs, receive a normalized risk summary, and review prior predictions in patient history.

## Highlights

- React frontend with a clean Apple-inspired clinical dashboard
- FastAPI backend with JWT-based demo authentication
- Risk prediction flows for diabetes and heart disease
- Unified prediction response format across both conditions
- Patient history tracking for signed-in users
- Backend and frontend test coverage for the current demo flow

## Tech Stack

- `back-end`: FastAPI service for login, risk prediction, and patient history
- `UI/healthcare-ai-ui`: React frontend for the demo workflow
- Frontend: React, Create React App
- Backend: FastAPI, Pydantic, python-jose
- ML: scikit-learn, pandas, joblib
- Testing: pytest, React Testing Library

## Project layout
## Project Structure

```text
healthcare-ai/
├── back-end/
│   ├── app/
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── predict.py
│   │   ├── predict_heart.py
│   │   ├── predict_router.py
│   │   ├── train_heart.py
│   │   ├── heart.csv
│   │   └── *.pkl
│   ├── tests/
│   └── requirements.txt
├── UI/healthcare-ai-ui/
├── UI/
│   └── healthcare-ai-ui/
├── train_model.py
└── test_predict.py
```

## Backend setup
## Features

- Login with a demo user ID and receive an auth token
- Submit diabetes risk inputs through the UI or API
- Submit heart-disease risk inputs through the UI or API
- View structured results with risk level, probability, and top factors
- Review prediction history for the active user

## Quick Start

### 1. Start the backend

From `/Users/chetanpallempati/Documents/New project/healthcare-ai/back-end`:
From the project root:

```bash
cd back-end
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:
Backend default URL:

- `JWT_SECRET`: token signing secret
- `TOKEN_TTL_HOURS`: token lifetime, defaults to `1`
- `ALLOWED_ORIGINS`: comma-separated frontend origins, defaults to local React dev URLs
```text
http://127.0.0.1:8000
```

API base URL: `http://127.0.0.1:8000`
### 2. Start the frontend

## Frontend setup
Open a second terminal:

From `/Users/chetanpallempati/Documents/New project/healthcare-ai/UI/healthcare-ai-ui`:

```bash
cd UI/healthcare-ai-ui
npm install
npm start
```

Optional environment variable:
Frontend default URL:

```text
http://localhost:3000
```

## Environment Variables

### Backend

- `JWT_SECRET`: JWT signing secret
- `TOKEN_TTL_HOURS`: token lifetime in hours, defaults to `1`
- `ALLOWED_ORIGINS`: comma-separated list of allowed frontend origins

Example:

```bash
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
export JWT_SECRET="change-this-secret"
export TOKEN_TTL_HOURS="1"
export ALLOWED_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
```

## Tests
### Frontend

- `REACT_APP_API_BASE_URL`: backend base URL

Backend:
Example:

```bash
cd /Users/chetanpallempati/Documents/New project/healthcare-ai/back-end
export REACT_APP_API_BASE_URL="http://127.0.0.1:8000"
```

## API Overview

### `POST /login`

Accepts:

```json
{
  "userId": "demo-user"
}
```

Returns:

```json
{
  "token": "..."
}
```

### `POST /predict-risk`

Requires authentication and accepts diabetes input fields.

### `POST /predict-heart`

Requires authentication and accepts heart-risk input fields.

### `POST /predict`

Generic multi-disease endpoint using:

```json
{
  "disease": "diabetes",
  "data": {}
}
```

### `GET /patient-history`

Returns prediction history for the authenticated user.

## Running Tests

### Backend

```bash
cd back-end
pytest -q
```

Frontend:
### Frontend

```bash
cd /Users/chetanpallempati/Documents/New project/healthcare-ai/UI/healthcare-ai-ui
cd UI/healthcare-ai-ui
npm test -- --watchAll=false
npm run build
```

## Model training
## Model Notes

### Heart model

The heart model can be retrained locally because the dataset is present at `back-end/app/heart.csv`.
- Trained from the local dataset at `back-end/app/heart.csv`
- Retrainable locally with:

```bash
cd /Users/chetanpallempati/Documents/New project/healthcare-ai
python back-end/app/train_heart.py
```

### Diabetes model

The diabetes model cannot be reliably regenerated from this repo alone right now because the original training dataset is not stored locally. `train_model.py` now expects a local CSV path in the Pima-style schema before it will write a new `model.pkl`.
- Uses a saved `model.pkl` artifact under `back-end/app/`
- The original training dataset is not stored in this repository
- `train_model.py` expects a local Pima-style CSV file path before retraining

Example:

```bash
python train_model.py --data /path/to/diabetes.csv
```

## Known limitation
## Current Limitations

The current `model.pkl` was created with a different `scikit-learn` version than the one in this environment, so you may still see a warning when the diabetes model loads. Regenerating that artifact requires the original source dataset.
- Authentication is still demo-oriented and does not use passwords
- Diabetes model reproducibility is incomplete because the source dataset is missing
- The diabetes `model.pkl` currently raises a scikit-learn version mismatch warning
- This project is suitable as a portfolio/demo app, not a clinical decision system

## Suggested Next Improvements

- Add real username/password authentication
- Store patient history in a persistent database
- Add model evaluation reports and calibration metrics
- Retrain the diabetes model from a versioned local dataset
- Add deployment configuration for the API and UI

## Status

Current local validation:

- `pytest -q`: passing
- `npm test -- --watchAll=false`: passing
- `npm run build`: passing

## Disclaimer

This project is for educational and demonstration purposes only. It is not intended for diagnosis, treatment, or real-world clinical decision-making.
