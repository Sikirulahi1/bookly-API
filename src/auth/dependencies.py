from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from src.config import secrets
from fastapi import Request
from src.auth.utils import decode_access_token
from fastapi.exceptions import HTTPException
from fastapi import status
from src.db.redis import token_in_blocklist

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super(TokenBearer, self).__call__(request)
        token = creds.credentials if creds else None
        token_data = decode_access_token(token) if token else None

        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                resolution="Please log in again",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if await token_in_blocklist(token_data.jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token is invalid or has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return token_data
    

class AccessTokenBearer(TokenBearer):
    
    def __init__(self, auto_error: bool = True):
        super(AccessTokenBearer, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token_data = await super(AccessTokenBearer, self).__call__(request)

        if token_data and token_data.refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token cannot be used as access token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data

class RefreshTokenBearer(TokenBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        token_data = await super(RefreshTokenBearer, self).__call__(request)
        if token_data and not token_data.refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token cannot be used as refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data