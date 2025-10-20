from fastapi.security import  HTTPBearer, HTTPAuthorizationCredentials
from src.config import secrets
from fastapi import Request, Depends
from src.auth.utils import decode_access_token
from fastapi.exceptions import HTTPException
from fastapi import status
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .service import AuthService

user_service = AuthService()

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
    

async def get_current_user(token_data: dict=Depends(AccessTokenBearer()), session: AsyncSession=Depends(get_session)):
    user_email = token_data.user.get("email")
    user =  await user_service.get_user_by_email(user_email, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user