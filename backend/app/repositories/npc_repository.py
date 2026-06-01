from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.npc import Npc
from app.models.map import MapNpc


class NpcRepository:
    """Repository para operaciones de NPC en base de datos"""

    @staticmethod
    def get_by_id(db: Session, npc_id: int) -> Npc | None:
        """Obtiene un NPC por su ID"""
        return db.query(Npc).filter(Npc.id == npc_id).first()

    @staticmethod
    def get_all(db: Session) -> list[Npc]:
        """Obtiene todos los NPCs"""
        return db.query(Npc).all()

    @staticmethod
    def get_by_map(db: Session, map_id: int) -> list[Npc]:
        """Obtiene todos los NPCs en un mapa específico"""
        return (
            db.query(Npc)
            .join(MapNpc, MapNpc.npc_id == Npc.id)
            .filter(MapNpc.map_id == map_id)
            .all()
        )

    @staticmethod
    def create(db: Session, name: str, role: str) -> Npc:
        """Crea un nuevo NPC"""
        npc = Npc(name=name, role=role)
        db.add(npc)
        db.commit()
        db.refresh(npc)
        return npc

    @staticmethod
    def update(db: Session, npc_id: int, **kwargs) -> Npc | None:
        """Actualiza un NPC"""
        npc = db.query(Npc).filter(Npc.id == npc_id).first()
        if not npc:
            return None
        for key, value in kwargs.items():
            if hasattr(npc, key):
                setattr(npc, key, value)
        db.commit()
        db.refresh(npc)
        return npc

    @staticmethod
    def delete(db: Session, npc_id: int) -> bool:
        """Elimina un NPC"""
        npc = db.query(Npc).filter(Npc.id == npc_id).first()
        if not npc:
            return False
        db.delete(npc)
        db.commit()
        return True

    @staticmethod
    def add_to_map(db: Session, npc_id: int, map_id: int) -> MapNpc:
        """Asigna un NPC a un mapa"""
        map_npc = MapNpc(npc_id=npc_id, map_id=map_id)
        db.add(map_npc)
        db.commit()
        db.refresh(map_npc)
        return map_npc

    @staticmethod
    def remove_from_map(db: Session, npc_id: int, map_id: int) -> bool:
        """Remueve un NPC de un mapa"""
        map_npc = (
            db.query(MapNpc)
            .filter(MapNpc.npc_id == npc_id, MapNpc.map_id == map_id)
            .first()
        )
        if not map_npc:
            return False
        db.delete(map_npc)
        db.commit()
        return True
