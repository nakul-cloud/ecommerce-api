from datetime import datetime, timedelta, timezone
import jwt
from app.config.settings import settings


def create_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Generate a new JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_jwt_token(token: str) -> dict | None:
    """
    Verify and decode a JWT token. Returns payload or None if invalid.
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload
    except jwt.PyJWTError:
        return None
