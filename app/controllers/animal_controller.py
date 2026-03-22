from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.schemas.animal_schema import CaptureIn
from app.services import animal_service


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
