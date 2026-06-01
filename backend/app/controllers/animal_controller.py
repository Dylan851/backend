from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.repositories import animal_repository
from app.schemas.animal_schema import CaptureIn
from app.services import animal_service


def list_animals(
    db: Session = Depends(get_db),
):
    animals = animal_repository.list_all(db)
    payload = [
        {"id": animal.id, "name": animal.name, "rarity": animal.rarity}
        for animal in animals
    ]
    return {"success": True, "data": {"animals": payload}}


def get_animal_detail(
    animal_id: int,
    db: Session = Depends(get_db),
):
    animal = animal_repository.get_by_id(db, animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return {
        "success": True,
        "data": {
            "id": animal.id,
            "name": animal.name,
            "rarity": animal.rarity,
        },
    }


def nearby_animals(
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    animals = animal_service.get_nearby(db, player.id)
    payload = [
        {"id": animal.id, "name": animal.name, "rarity": animal.rarity}
        for animal in animals
    ]
    return {"success": True, "data": {"animals": payload}}


def capture_animal(
    payload: CaptureIn,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    capture = animal_service.capture(db, player.id, payload.animal_id)
    return {
        "success": True,
        "data": {
            "capture_id": capture.id,
            "animal_id": capture.animal_id,
            "captured_at": capture.captured_at,
        },
    }


def capture_animal_by_path(
    animal_id: int,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    capture = animal_service.capture(db, player.id, animal_id)
    return {
        "success": True,
        "data": {
            "animal_id": capture.animal_id,
            "captured_at": capture.captured_at,
        },
    }
