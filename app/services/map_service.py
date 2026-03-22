from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.map import Map, PlayerMapUnlocked
from app.repositories import player_repository


def list_maps(db: Session):
    return db.query(Map).all()


def list_unlocked(db: Session, player_id: int):
    return (
        db.query(Map)
        .join(PlayerMapUnlocked, PlayerMapUnlocked.map_id == Map.id)
        .filter(PlayerMapUnlocked.player_id == player_id)
        .all()
    )


def unlock_map(db: Session, player_id: int, map_id: int):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    game_map = db.query(Map).filter(Map.id == map_id).first()
    if not game_map:
        raise HTTPException(status_code=404, detail="Map not found")
    if player.level < game_map.required_level:
        raise HTTPException(status_code=400, detail="Player level too low")
    already = (
        db.query(PlayerMapUnlocked)
        .filter(PlayerMapUnlocked.player_id == player_id, PlayerMapUnlocked.map_id == map_id)
        .first()
    )
    if already:
        return already
    unlocked = PlayerMapUnlocked(player_id=player_id, map_id=map_id)
    db.add(unlocked)
    db.commit()
    db.refresh(unlocked)
    return unlocked
