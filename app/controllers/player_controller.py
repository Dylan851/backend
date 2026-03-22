from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.schemas.player_schema import PlayerLocationUpdate
from app.services import player_service


def get_profile(
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    profile = player_service.get_profile(db, player.id)
    return {"success": True, "data": profile}


def update_location(
    payload: PlayerLocationUpdate,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    profile = player_service.update_location(db, player.id, payload.coord_lat, payload.coord_lng)
    return {"success": True, "data": profile}


def get_inventory(
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    inventory = player_service.get_inventory(db, player.id)
    return {"success": True, "data": {"inventory": inventory}}
