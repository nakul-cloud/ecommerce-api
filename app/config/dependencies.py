from fastapi import Depends,Header,HTTPException,status
from app.config.settings import ADMIN_API_KEY

def verify_admin_api_key(
    x_api_key:str = Header(...)
):
    """
    Verify the adminstrator API Key
    """
    if x_api_key!=ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Admin API key"
        )
    return True 