from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.services import map_service


def list_maps(db: Session = Depends(get_db)):
    maps = map_service.list_maps(db)
    payload = [
        {"id": game_map.id, "name": game_map.name, "required_level": game_map.required_level}
        for game_map in maps
    ]
    return {"success": True, "data": {"maps": payload}}


def list_unlocked_maps(
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    maps = map_service.list_unlocked(db, player.id)
    payload = [
        {"id": game_map.id, "name": game_map.name, "required_level": game_map.required_level}
        for game_map in maps
    ]
    return {"success": True, "data": {"maps": payload}}


def unlock_map(
    map_id: int,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    unlocked = map_service.unlock_map(db, player.id, map_id)
    return {
        "success": True,
        "data": {
            "unlocked_id": unlocked.id,
            "map_id": unlocked.map_id,
        },
    }
