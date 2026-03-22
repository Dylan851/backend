from sqlalchemy.orm import Session

from app.models.animal import Animal, Capture, MapAnimal


def list_by_map(db: Session, map_id: int):
    return (
        db.query(Animal)
        .join(MapAnimal, MapAnimal.animal_id == Animal.id)
        .filter(MapAnimal.map_id == map_id)
        .all()
    )


def get_by_id(db: Session, animal_id: int) -> Animal | None:
    return db.query(Animal).filter(Animal.id == animal_id).first()


def create_capture(db: Session, player_id: int, animal_id: int) -> Capture:
    capture = Capture(player_id=player_id, animal_id=animal_id)
    db.add(capture)
    db.commit()
    db.refresh(capture)
    return capture


def already_captured(db: Session, player_id: int, animal_id: int) -> bool:
    return (
        db.query(Capture)
        .filter(Capture.player_id == player_id, Capture.animal_id == animal_id)
        .first()
        is not None
    )
