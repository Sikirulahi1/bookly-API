from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
from .schemas import TokenData
from datetime import datetime, timedelta, timezone
from src.config import secrets
import uuid
import logging

# password hashing utils
password_hash = PasswordHash.recommended()

def generate_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

# jwt authentication utils
def create_access_token(user_data: dict, expires_delta: timedelta | None = None, refresh: bool = False) -> str:
    payload = user_data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=secrets.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"expiry": expire})
    payload.update({"jti": str(uuid.uuid4())})
    payload.update({"refresh": refresh})
    encoded_token = jwt.encode(payload, secrets.JWT_SECRET_KEY, algorithm=secrets.JWT_ALGORITHM)
    return encoded_token


def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, secrets.JWT_SECRET_KEY, algorithms=[secrets.JWT_ALGORITHM])
        token_data = TokenData(**payload)
        return token_data
    except jwt.PyJWTError as e:
        logging.exception("Token decoding failed", exc_info=e)
        return None

