from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    identifier: str
    password: str


class GoogleAuthRequest(BaseModel):
    id_token: str


class SupabaseAuthRequest(BaseModel):
    access_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
