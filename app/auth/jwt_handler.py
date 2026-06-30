from typing import Any
from app.utils.jwt import create_jwt_token, verify_jwt_token
from app.exceptions.custom_exceptions import InvalidTokenException


def create_access_token(data: dict[str, Any]) -> str:
    """
    Create a JWT access token.
    """
    return create_jwt_token(data)


def verify_access_token(token: str) -> dict[str, Any]:
    """
    Verify and decode a JWT access token.
    """
    payload = verify_jwt_token(token)
    if payload is None:
        raise InvalidTokenException()
    return payload