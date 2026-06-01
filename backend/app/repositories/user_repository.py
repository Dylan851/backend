from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.user import User
from app.models.player import Player


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_by_identifier(db: Session, identifier: str) -> User | None:
    return (
        db.query(User)
        .outerjoin(Player, User.player_id == Player.id)
        .filter(or_(User.email == identifier, Player.nickname == identifier))
        .first()
    )


def create_user(
    db: Session,
    email: str,
    password_hash: str,
    player_id: int | None = None,
    has_password: bool = True,
    has_google: bool = False,
) -> User:
    user = User(
        email=email,
        password_hash=password_hash,
        player_id=player_id,
        has_password=has_password,
        has_google=has_google,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def attach_player(db: Session, user: User, player_id: int) -> User:
    user.player_id = player_id
    db.commit()
    db.refresh(user)
    return user


def update_auth_methods(
    db: Session,
    user: User,
    *,
    has_password: bool | None = None,
    has_google: bool | None = None,
) -> User:
    if has_password is not None:
        user.has_password = has_password
    if has_google is not None:
        user.has_google = has_google
    db.commit()
    db.refresh(user)
    return user
