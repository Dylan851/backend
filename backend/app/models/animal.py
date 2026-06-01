from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, literal
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from app.config.database import Base


class Animal(Base):
    __tablename__ = "animales"

    id = Column("id_animal", Integer, primary_key=True, index=True)
    name = Column("nombre", String(150), nullable=False)
    tipo = Column("tipo", String(50), nullable=True)  # Tipo de animal (del script SQL)
    # En la BD actual no existe rarity; usamos None en runtime.
    rarity = column_property(literal(None))

    captures = relationship("Capture", back_populates="animal")
    map_links = relationship("MapAnimal", back_populates="animal")


class Capture(Base):
    __tablename__ = "captura"

    player_id = Column("id_jugador", Integer, ForeignKey("jugador.id_jugador"), primary_key=True)
    animal_id = Column("id_animal", Integer, ForeignKey("animales.id_animal"), primary_key=True)
    captured_at = column_property(literal(None))

    player = relationship("Player", back_populates="captures")
    animal = relationship("Animal", back_populates="captures")


class MapAnimal(Base):
    __tablename__ = "mapa_animales"

    map_id = Column("id_mapa", Integer, ForeignKey("mapa.id_mapa"), primary_key=True)
    animal_id = Column("id_animal", Integer, ForeignKey("animales.id_animal"), primary_key=True)

    animal = relationship("Animal", back_populates="map_links")
    game_map = relationship("Map", back_populates="animal_links")
