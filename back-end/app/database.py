# For demo, we’ll use in-memory store. In production, use Redis or Postgres.
PATIENT_HISTORY = {}

def add_history(user_id: str, data: dict):
    if user_id not in PATIENT_HISTORY:
        PATIENT_HISTORY[user_id] = []
    PATIENT_HISTORY[user_id].append(data)

def get_history(user_id: str):
    return PATIENT_HISTORY.get(user_id, [])