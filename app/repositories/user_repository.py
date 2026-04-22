from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.models.player import Player


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_identifier(db: Session, identifier: str) -> User | None:
    return (
        db.query(User)
        .outerjoin(Player, User.player_id == Player.id)
        .filter(or_(User.email == identifier, Player.nickname == identifier))
        .first()
    )


def create_user(db: Session, email: str, password_hash: str, player_id: int | None = None) -> User:
    user = User(email=email, password_hash=password_hash, player_id=player_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def attach_player(db: Session, user: User, player_id: int) -> User:
    user.player_id = player_id
    db.commit()
    db.refresh(user)
    return user
