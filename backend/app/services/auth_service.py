import secrets
from typing import Any

import requests
from fastapi import HTTPException, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.repositories import player_repository, user_repository
from app.services import player_service
from app.utils.jwt_handler import create_access_token
from app.utils.password_utils import hash_password, verify_password

GENERIC_RECOVERY_MESSAGE = (
    "Si existe una cuenta con este correo, recibiras instrucciones para restablecer tu contrasena."
)
GOOGLE_ONLY_MESSAGE = (
    "Esta cuenta inicia sesion con Google. Usa el boton de Google para acceder."
)


def normalize_email(email: str) -> str:
    return (email or "").strip().lower()


def get_auth_methods_by_email(db: Session, email: str) -> dict[str, Any]:
    normalized_email = normalize_email(email)
    if not normalized_email:
        raise HTTPException(status_code=400, detail="El correo es obligatorio.")

    user = user_repository.get_by_email(db, normalized_email)
    if not user:
        return {
            "email": normalized_email,
            "exists": False,
            "has_password": False,
            "has_google": False,
        }

    return {
        "email": normalized_email,
        "exists": True,
        "has_password": bool(user.has_password),
        "has_google": bool(user.has_google),
    }


def register(db: Session, email: str, username: str, password: str):
    normalized_email = normalize_email(email)
    existing_user = user_repository.get_by_email(db, normalized_email)
    if existing_user:
        if existing_user.has_google and not existing_user.has_password:
            raise HTTPException(
                status_code=400,
                detail=(
                    "Este correo ya existe con Google. "
                    "Inicia con Google para continuar o anadir contrasena."
                ),
            )
        raise HTTPException(
            status_code=400,
            detail="Este correo ya esta registrado. Inicia sesion.",
        )

    normalized_username = (username or "").strip()
    if normalized_username and user_repository.get_by_identifier(db, normalized_username):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya esta en uso.")

    user = user_repository.create_user(
        db,
        normalized_email,
        hash_password(password),
        has_password=True,
        has_google=False,
    )
    nickname = normalized_username or normalized_email.split("@")[0]
    player = player_repository.create_player(db, nickname=nickname)
    user_repository.attach_player(db, user, player.id)

    return _build_session_response(db, user.id, player)


def login(db: Session, identifier: str, password: str):
    normalized_identifier = normalize_email(identifier) if "@" in (identifier or "") else (identifier or "").strip()
    user = user_repository.get_by_identifier(db, normalized_identifier)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contrasena incorrectos.",
        )

    if not user.has_password and user.has_google:
        raise HTTPException(status_code=400, detail=GOOGLE_ONLY_MESSAGE)

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contrasena incorrectos.",
        )

    player = _ensure_player_for_user(db, user.id, normalized_identifier)
    return _build_session_response(db, user.id, player)


def login_with_google(db: Session, raw_id_token: str):
    claims = _verify_google_id_token(raw_id_token)
    email = normalize_email((claims.get("email") or ""))
    if not email:
        raise HTTPException(status_code=400, detail="Google token missing email")

    preferred_name = _preferred_name_from_google_claims(claims, email)
    user, player = _upsert_social_user(
        db=db,
        email=email,
        preferred_name=preferred_name,
        metadata_name=(claims.get("name") or "").strip(),
    )
    return _build_session_response(db, user.id, player)


def login_with_supabase(db: Session, access_token: str):
    claims = _fetch_supabase_user_claims(access_token)
    email = normalize_email((claims.get("email") or ""))
    if not email:
        raise HTTPException(status_code=400, detail="Supabase token missing email")

    metadata = claims.get("user_metadata") or {}
    preferred_name = (
        (metadata.get("full_name") or "").strip()
        or (metadata.get("name") or "").strip()
        or email.split("@")[0]
    )
    user, player = _upsert_social_user(
        db=db,
        email=email,
        preferred_name=preferred_name,
        metadata_name=(metadata.get("full_name") or metadata.get("name") or "").strip(),
    )
    return _build_session_response(db, user.id, player)


def request_password_recovery(db: Session, email: str) -> str:
    status_data = get_auth_methods_by_email(db, email)
    if not status_data["exists"]:
        return GENERIC_RECOVERY_MESSAGE

    has_password = status_data["has_password"]
    has_google = status_data["has_google"]
    if has_password and has_google:
        return (
            "Te enviaremos instrucciones para restablecer la contrasena de acceso manual. "
            "Esto no cambia tu cuenta de Google."
        )
    if has_password:
        return GENERIC_RECOVERY_MESSAGE
    if has_google:
        raise HTTPException(status_code=400, detail=GOOGLE_ONLY_MESSAGE)

    return GENERIC_RECOVERY_MESSAGE


def _ensure_player_for_user(db: Session, user_id: int, identifier: str):
    player = player_repository.get_by_user_id(db, user_id)
    if not player:
        nickname = identifier.split("@")[0] if "@" in identifier else identifier
        player = player_repository.create_player(db, nickname=nickname)
        user = user_repository.get_by_id(db, user_id)
        if user:
            user_repository.attach_player(db, user, player.id)
    elif not (player.nickname or "").strip():
        nickname = identifier.split("@")[0] if "@" in identifier else identifier
        player_repository.update_profile(db, player, nickname=nickname)
    return player


def _upsert_social_user(db: Session, email: str, preferred_name: str, metadata_name: str):
    user = user_repository.get_by_email(db, email)
    if not user:
        user = user_repository.create_user(
            db,
            email=email,
            password_hash=hash_password(secrets.token_urlsafe(32)),
            has_password=False,
            has_google=True,
        )
    elif not user.has_google:
        user = user_repository.update_auth_methods(db, user, has_google=True)

    player = player_repository.get_by_user_id(db, user.id)
    if not player:
        player = player_repository.create_player(db, nickname=preferred_name)
        user_repository.attach_player(db, user, player.id)
    else:
        current_nick = (player.nickname or "").strip()
        email_prefix = email.split("@")[0]
        if (
            not current_nick
            or current_nick.lower() == (metadata_name or "").lower()
            or current_nick.lower() == email_prefix.lower()
        ):
            player_repository.update_profile(db, player, nickname=preferred_name)
    return user, player


def _build_session_response(db: Session, user_id: int, player: Any) -> dict[str, Any]:
    token = create_access_token({"sub": str(user_id)})
    profile = player_service.build_profile(db, player)
    return {"token": token, "player": profile}


def _preferred_name_from_google_claims(claims: dict[str, Any], email: str) -> str:
    given_name = (claims.get("given_name") or "").strip()
    full_name = (claims.get("name") or "").strip()
    if given_name:
        return given_name.split()[0]
    if full_name:
        return full_name.split()[0]
    return email.split("@")[0]


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
