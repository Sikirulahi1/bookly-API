from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from src.config import secrets
from fastapi import Request
from src.auth.utils import decode_access_token
from fastapi.exceptions import HTTPException
from fastapi import status

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AccessTokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super(AccessTokenBearer, self).__call__(request)
        token = creds.credentials if creds else None
        token_data = decode_access_token(token) if token else None

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if token_data.refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token cannot be used for accessing resources",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token_data
    

