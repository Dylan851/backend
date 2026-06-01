from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.enemigo import Enemigo
from app.models.npc import Npc
from app.models.map import MapNpc


class EnemyRepository:
    """Repository para operaciones de Enemigos en base de datos"""

    @staticmethod
    def get_by_id(db: Session, enemy_id: int) -> Enemigo | None:
        """Obtiene un Enemigo por su ID"""
        return db.query(Enemigo).filter(Enemigo.id_npc == enemy_id).first()

    @staticmethod
    def get_all(db: Session) -> list[Enemigo]:
        """Obtiene todos los Enemigos"""
        return db.query(Enemigo).all()

    @staticmethod
    def get_by_map(db: Session, map_id: int) -> list[Enemigo]:
        """Obtiene todos los Enemigos en un mapa específico"""
        return (
            db.query(Enemigo)
            .join(Npc, Enemigo.id_npc == Npc.id)
            .join(MapNpc, MapNpc.npc_id == Npc.id)
            .filter(MapNpc.map_id == map_id)
            .all()
        )

    @staticmethod
    def get_by_level(db: Session, nivel: int) -> list[Enemigo]:
        """Obtiene todos los Enemigos de un nivel específico"""
        return db.query(Enemigo).filter(Enemigo.nivel == nivel).all()

    @staticmethod
    def create(db: Session, name: str, nivel: int, dano: int) -> Enemigo:
        """Crea un nuevo Enemigo"""
        npc = Npc(name=name, role="Enemigo")
        db.add(npc)
        db.flush()  # Flush para obtener el ID sin hacer commit

        enemy = Enemigo(id_npc=npc.id, nivel=nivel, dano=dano)
        db.add(enemy)
        db.commit()
        db.refresh(enemy)
        return enemy

    @staticmethod
    def update(db: Session, enemy_id: int, **kwargs) -> Enemigo | None:
        """Actualiza un Enemigo"""
        enemy = db.query(Enemigo).filter(Enemigo.id_npc == enemy_id).first()
        if not enemy:
            return None
        for key, value in kwargs.items():
            if hasattr(enemy, key):
                setattr(enemy, key, value)
        db.commit()
        db.refresh(enemy)
        return enemy

    @staticmethod
    def delete(db: Session, enemy_id: int) -> bool:
        """Elimina un Enemigo"""
        enemy = db.query(Enemigo).filter(Enemigo.id_npc == enemy_id).first()
        if not enemy:
            return False
        npc = db.query(Npc).filter(Npc.id == enemy_id).first()
        if npc:
            db.delete(npc)
        db.commit()
        return True

    @staticmethod
    def add_to_map(db: Session, enemy_id: int, map_id: int) -> MapNpc:
        """Asigna un Enemigo a un mapa"""
        map_npc = MapNpc(npc_id=enemy_id, map_id=map_id)
        db.add(map_npc)
        db.commit()
        db.refresh(map_npc)
        return map_npc
