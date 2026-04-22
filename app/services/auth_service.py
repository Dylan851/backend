from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories import user_repository, player_repository
from app.services import player_service
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_handler import create_access_token


def register(db: Session, email: str, username: str, password: str):
    if user_repository.get_by_identifier(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if username and user_repository.get_by_identifier(db, username):
        raise HTTPException(status_code=400, detail="Username already registered")

    user = user_repository.create_user(db, email, hash_password(password))
    nickname = username or email.split("@")[0]
    player = player_repository.create_player(db, nickname=nickname)
    user_repository.attach_player(db, user, player.id)

    token = create_access_token({"sub": str(user.id)})
    profile = player_service.build_profile(db, player)

    return {"token": token, "player": profile}


def login(db: Session, identifier: str, password: str):
    user = user_repository.get_by_identifier(db, identifier)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    player = player_repository.get_by_user_id(db, user.id)
    if not player:
        nickname = identifier.split("@")[0] if "@" in identifier else identifier
        player = player_repository.create_player(db, nickname=nickname)
        user_repository.attach_player(db, user, player.id)

    token = create_access_token({"sub": str(user.id)})
    profile = player_service.build_profile(db, player)

    return {"token": token, "player": profile}
