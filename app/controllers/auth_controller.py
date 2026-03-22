from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin
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
