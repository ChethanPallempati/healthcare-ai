# Healthcare AI

This repository contains:

- `back-end`: FastAPI service for login, risk prediction, and patient history
- `UI/healthcare-ai-ui`: React frontend for the demo workflow

## Project layout

```text
healthcare-ai/
├── back-end/
│   ├── app/
│   ├── tests/
│   └── requirements.txt
├── UI/healthcare-ai-ui/
├── train_model.py
└── test_predict.py
```

## Backend setup

From `/Users/chetanpallempati/Documents/New project/healthcare-ai/back-end`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables:

- `JWT_SECRET`: token signing secret
- `TOKEN_TTL_HOURS`: token lifetime, defaults to `1`
- `ALLOWED_ORIGINS`: comma-separated frontend origins, defaults to local React dev URLs

API base URL: `http://127.0.0.1:8000`

## Frontend setup

From `/Users/chetanpallempati/Documents/New project/healthcare-ai/UI/healthcare-ai-ui`:

```bash
npm install
npm start
```

Optional environment variable:

```bash
REACT_APP_API_BASE_URL=http://127.0.0.1:8000
```


## Model training

### Heart model

The heart model can be retrained locally because the dataset is present at `back-end/app/heart.csv`.
end/app/train_heart.py

### Diabetes model

The diabetes model cannot be reliably regenerated from this repo alone right now because the original training dataset is not stored locally. `train_model.py` now expects a local CSV path in the Pima-style schema before it will write a new `model.pkl`.

## Known limitation

The current `model.pkl` was created with a different `scikit-learn` version than the one in this environment, so you may still see a warning when the diabetes model loads. Regenerating that artifact requires the original source dataset.
