from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    password: str


class UserLogin(BaseModel):
    identifier: str
    password: str


class EmailLookupRequest(BaseModel):
    email: EmailStr


class GoogleAuthRequest(BaseModel):
    id_token: str


class SupabaseAuthRequest(BaseModel):
    access_token: str


class PasswordRecoveryRequest(BaseModel):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

    class Config:
        from_attributes = True
