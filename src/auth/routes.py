from fastapi import APIRouter
from src.db.redis import add_jti_to_blocklist
from .schemas import UserCreateModel, UserLoginModel
from .service import AuthService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from .schemas import UserModel
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta, datetime, timezone
from fastapi.responses import JSONResponse
from .dependencies import AccessTokenBearer, RefreshTokenBearer, get_current_user, RoleChecker



auth_router = APIRouter()
auth_service = AuthService()
role_checker = RoleChecker(allowed_roles=["admin", "user"])

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    user_exists = await auth_service.user_exist(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="user with email already exists")
    
    new_user = await auth_service.create_user(user_data, session)
    return new_user

@auth_router.post("/login")
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await auth_service.get_user_by_email(email, session)
    if user is not None:
        is_password_valid = verify_password(password, user.password_hash)
        if is_password_valid:
            user_data = {
                "user_uid": str(user.uid),
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
            access_token = create_access_token(user_data)
            refresh_token = create_access_token(user_data, refresh=True, expiry= timedelta(days=7))
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "user": {
                        "uid": str(user.uid),
                        "username": user.username,
                        "email": user.email
                    }
                }
            )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

@auth_router.post("/refresh-token")
async def refresh_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details.exp
    print(expiry_timestamp)

    if expiry_timestamp > datetime.now(timezone.utc):
        new_access_token = create_access_token(
            {
                "user_uid": token_details.user.get("user_uid"),
                "username": token_details.user.get("username"), 
                "email": token_details.user.get("email"),
            }
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "access_token": new_access_token,
                "token_type": "bearer"
            }
        )
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token has expired")

@auth_router.get("/me", response_model=UserModel)
async def get_current_user(user = Depends(get_current_user), _:bool=Depends(role_checker)):
    return user

@auth_router.post("/logout")
async def logout_user(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details.jti
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Logout successful"
        }
    )
