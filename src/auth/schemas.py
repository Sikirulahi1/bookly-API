from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=30)
    last_name: str = Field(max_length=30)
    username: str = Field(max_length=8)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8)


class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool  
    password_hash: str = Field(exclude=True)
    created_at: datetime 
    updated_at: datetime 
