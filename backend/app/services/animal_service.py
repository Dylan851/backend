from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import animal_repository, player_repository


def get_nearby(db: Session, player_id: int):
    player = player_repository.get_by_id(db, player_id)
    if not player or not player.current_map_id:
        raise HTTPException(status_code=404, detail="Player or current map not found")
    return animal_repository.list_by_map(db, player.current_map_id)


def capture(db: Session, player_id: int, animal_id: int):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    animal = animal_repository.get_by_id(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    if animal_repository.already_captured(db, player_id, animal_id):
        raise HTTPException(status_code=400, detail="Animal already captured")
    return animal_repository.create_capture(db, player_id, animal_id)
