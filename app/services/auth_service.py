from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
import secrets
import requests

from app.repositories import user_repository, player_repository
from app.services import player_service
from app.utils.password_utils import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.config.settings import settings


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
    elif not (player.nickname or "").strip():
        nickname = identifier.split("@")[0] if "@" in identifier else identifier
        player_repository.update_profile(db, player, nickname=nickname)

    token = create_access_token({"sub": str(user.id)})
    profile = player_service.build_profile(db, player)

    return {"token": token, "player": profile}


def login_with_google(db: Session, raw_id_token: str):
    claims = _verify_google_id_token(raw_id_token)
    email = (claims.get("email") or "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="Google token missing email")

    user = user_repository.get_by_identifier(db, email)
    if not user:
        # Create a local user linked to Google email. Password is random and unknown.
        user = user_repository.create_user(
            db,
            email=email,
            password_hash=hash_password(secrets.token_urlsafe(32)),
        )

    player = player_repository.get_by_user_id(db, user.id)
    given_name = (claims.get("given_name") or "").strip()
    full_name = (claims.get("name") or "").strip()
    first_name = ""
    if given_name:
        first_name = given_name.split()[0]
    elif full_name:
        first_name = full_name.split()[0]
    preferred_name = first_name or email.split("@")[0]
    if not player:
        player = player_repository.create_player(db, nickname=preferred_name)
        user_repository.attach_player(db, user, player.id)
    else:
        current_nick = (player.nickname or "").strip()
        email_prefix = email.split("@")[0]
        if (
            not current_nick
            or current_nick.lower() == full_name.lower()
            or current_nick.lower() == email_prefix.lower()
        ):
            player_repository.update_profile(db, player, nickname=preferred_name)

    token = create_access_token({"sub": str(user.id)})
    profile = player_service.build_profile(db, player)
    return {"token": token, "player": profile}


def login_with_supabase(db: Session, access_token: str):
    claims = _fetch_supabase_user_claims(access_token)
    email = (claims.get("email") or "").strip().lower()
    if not email:
        raise HTTPException(status_code=400, detail="Supabase token missing email")

    user = user_repository.get_by_identifier(db, email)
    if not user:
        user = user_repository.create_user(
            db,
            email=email,
            password_hash=hash_password(secrets.token_urlsafe(32)),
        )

    player = player_repository.get_by_user_id(db, user.id)
    metadata = claims.get("user_metadata") or {}
    preferred_name = (
        (metadata.get("full_name") or "").strip()
        or (metadata.get("name") or "").strip()
        or email.split("@")[0]
    )
    if not player:
        player = player_repository.create_player(db, nickname=preferred_name)
        user_repository.attach_player(db, user, player.id)
    elif not (player.nickname or "").strip():
        player_repository.update_profile(db, player, nickname=preferred_name)

    token = create_access_token({"sub": str(user.id)})
    profile = player_service.build_profile(db, player)
    return {"token": token, "player": profile}


def _verify_google_id_token(raw_id_token: str) -> dict:
    client_ids = [v.strip() for v in settings.GOOGLE_CLIENT_IDS.split(",") if v.strip()]
    if not client_ids:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth is not configured on server",
        )

    last_error = None
    for client_id in client_ids:
        try:
            claims = google_id_token.verify_oauth2_token(
                raw_id_token,
                google_requests.Request(),
                client_id,
            )
            issuer = claims.get("iss")
            if issuer not in {"accounts.google.com", "https://accounts.google.com"}:
                raise HTTPException(status_code=401, detail="Invalid Google token issuer")
            return claims
        except Exception as exc:  # noqa: BLE001
            last_error = exc

    raise HTTPException(status_code=401, detail=f"Invalid Google token: {last_error}")


def _fetch_supabase_user_claims(access_token: str) -> dict:
    supabase_url = settings.SUPABASE_URL.strip().rstrip("/")
    supabase_anon_key = settings.SUPABASE_ANON_KEY.strip()
    if not supabase_url or not supabase_anon_key:
        raise HTTPException(status_code=500, detail="Supabase is not configured on server")

    response = requests.get(
        f"{supabase_url}/auth/v1/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "apikey": supabase_anon_key,
        },
        timeout=10,
    )
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Supabase access token")
    payload = response.json()
    if not isinstance(payload, dict):
        raise HTTPException(status_code=401, detail="Invalid Supabase user payload")
    return payload
