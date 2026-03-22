from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class Map(Base):
    __tablename__ = "Mapa"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    zona = Column(String(100), nullable=True)  # Zona del mapa (del script SQL)
    required_level = Column(Integer, default=1, nullable=False)

    animal_links = relationship("MapAnimal", back_populates="game_map")
    npc_links = relationship("MapNpc", back_populates="game_map")
    item_links = relationship("MapItem", back_populates="game_map")
    unlocked_by_players = relationship("PlayerMapUnlocked", back_populates="game_map")


class PlayerMapUnlocked(Base):
    __tablename__ = "Jugador_Mapa_Desbloqueado"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("Jugador.id"), nullable=False)
    map_id = Column(Integer, ForeignKey("Mapa.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("Player", back_populates="unlocked_maps")
    game_map = relationship("Map", back_populates="unlocked_by_players")


class MapNpc(Base):
    __tablename__ = "Mapa_NPC"

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey("Mapa.id"), nullable=False)
    npc_id = Column(Integer, ForeignKey("NPC.id"), nullable=False)

    game_map = relationship("Map", back_populates="npc_links")
    npc = relationship("Npc", back_populates="map_links")


class MapItem(Base):
    __tablename__ = "Mapa_Item"

    id = Column(Integer, primary_key=True, index=True)
    map_id = Column(Integer, ForeignKey("Mapa.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    quantity_available = Column(Integer, default=1, nullable=False)

    game_map = relationship("Map", back_populates="item_links")
    item = relationship("Item", back_populates="map_links")
