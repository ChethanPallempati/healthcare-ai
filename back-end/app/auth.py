import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Header, HTTPException
from jose import JWTError, jwt

JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-secret-change-me")
ALGORITHM = "HS256"
TOKEN_TTL_HOURS = int(os.getenv("TOKEN_TTL_HOURS", "1"))


def create_token(user_id: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS)
    payload = {"userId": user_id, "exp": expiration}
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def authenticate(
    authorization: Optional[str] = Header(default=None, description="Bearer token"),
    token: Optional[str] = Header(default=None, description="Legacy token header"),
) -> str:
    raw_token = authorization or token

    if not raw_token:
        raise HTTPException(status_code=401, detail="Missing token")

    if raw_token.startswith("Bearer "):
        raw_token = raw_token[7:]

    try:
        payload = jwt.decode(raw_token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload["userId"]
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc
