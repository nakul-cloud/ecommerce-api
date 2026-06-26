from app.exceptions.custom_exceptions import InvalidTokenException
from datetime import datetime,timedelta,timezone
from typing import Any

from jose import JWTError,jwt

from app.config.settings import(
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

def create_access_token(data:dict[str,Any])-> str:
    """
    Create a JWT access token.
    """

    # Copy Payload
    payload = data.copy()

    # Token expiration time
    expire = datetime.now(timezone.utc)+timedelta(
        minutes = ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # ADD expiration claim
    payload.update(
        {
            "exp":expire
        }
    )

    # Generate JWT
    access_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return access_token

    def verify_access_token(token:str)-> dict[str,Any]:
        """
        Verify and decode a JWT token.
        """
        try:
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
            )
            return payload
            
        except JWTError:
            raise InvalidTokenException()
    
    