from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.user_schema import (
    EmailLookupRequest,
    GoogleAuthRequest,
    PasswordRecoveryRequest,
    SupabaseAuthRequest,
    UserCreate,
    UserLogin,
)
from app.services import auth_service


def register(payload: UserCreate, db: Session = Depends(get_db)):
    result = auth_service.register(db, payload.email, payload.username, payload.password)
    return {
        "success": True,
        "data": {
            "token": result["token"],
            "player": result["player"],
        },
    }


def login(payload: UserLogin, db: Session = Depends(get_db)):
    result = auth_service.login(db, payload.identifier, payload.password)
    return {
        "success": True,
        "data": {
            "token": result["token"],
            "player": result["player"],
        },
    }


def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    result = auth_service.login_with_google(db, payload.id_token)
    return {
        "success": True,
        "data": {
            "token": result["token"],
            "player": result["player"],
        },
    }


def supabase_auth(payload: SupabaseAuthRequest, db: Session = Depends(get_db)):
    result = auth_service.login_with_supabase(db, payload.access_token)
    return {
        "success": True,
        "data": {
            "token": result["token"],
            "player": result["player"],
        },
    }


def auth_methods(payload: EmailLookupRequest, db: Session = Depends(get_db)):
    result = auth_service.get_auth_methods_by_email(db, payload.email)
    return {"success": True, "data": result}


def recover_password(payload: PasswordRecoveryRequest, db: Session = Depends(get_db)):
    message = auth_service.request_password_recovery(db, payload.email)
    return {
        "success": True,
        "message": message,
        "data": {"message": message},
    }
