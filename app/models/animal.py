from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class Animal(Base):
    __tablename__ = "Animales"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    tipo = Column(String(50), nullable=True)  # Tipo de animal (del script SQL)
    rarity = Column(String(50), nullable=True)

    captures = relationship("Capture", back_populates="animal")
    map_links = relationship("MapAnimal", back_populates="animal")


class Capture(Base):
    __tablename__ = "Captura"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("Jugador.id"), nullable=False)
    animal_id = Column(Integer, ForeignKey("Animales.id"), nullable=False)
    captured_at = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("Player", back_populates="captures")
    animal = relationship("Animal", back_populates="captures")


class MapAnimal(Base):
    __tablename__ = "Mapa_Animales"

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey("Mapa.id"), nullable=False)
    animal_id = Column(Integer, ForeignKey("Animales.id"), nullable=False)

    animal = relationship("Animal", back_populates="map_links")
    game_map = relationship("Map", back_populates="animal_links")
