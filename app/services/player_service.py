from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import player_repository


def build_profile(db: Session, player):
    return {
        "id": player.id,
        "nickname": player.nickname,
        "level": player.level,
        "coins": player.coins,
        "gems": player.gems,
        "coord_lat": player.coord_lat,
        "coord_lng": player.coord_lng,
        "current_map_id": player.current_map_id,
        "inventory": player_repository.get_inventory(db, player.id),
        "captured_animals": player_repository.get_captured_animals(db, player.id),
        "unlocked_maps": player_repository.get_unlocked_maps(db, player.id),
    }


def get_profile(db: Session, player_id: int):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return build_profile(db, player)


def update_location(db: Session, player_id: int, coord_lat: float, coord_lng: float):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_repository.update_location(db, player, coord_lat, coord_lng)
    return build_profile(db, player)


def update_profile(
    db: Session,
    player_id: int,
    *,
    nickname: str | None = None,
    coins: int | None = None,
    gems: int | None = None,
):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    player_repository.update_profile(
        db,
        player,
        nickname=nickname,
        coins=coins,
        gems=gems,
    )
    return build_profile(db, player)


def get_inventory(db: Session, player_id: int):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player_repository.get_inventory(db, player.id)
