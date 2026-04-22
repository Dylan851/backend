from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, literal
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from app.config.database import Base


class Map(Base):
    __tablename__ = "mapa"

    id = Column("id_mapa", Integer, primary_key=True, index=True)
    name = Column("nombre", String(150), nullable=False)
    zona = Column("zona", String(100), nullable=True)  # Zona del mapa (del script SQL)
    # En la BD actual no existe required_level; usamos un valor por defecto en runtime.
    required_level = column_property(literal(1))

    animal_links = relationship("MapAnimal", back_populates="game_map")
    npc_links = relationship("MapNpc", back_populates="game_map")
    item_links = relationship("MapItem", back_populates="game_map")
    unlocked_by_players = relationship("PlayerMapUnlocked", back_populates="game_map")


class PlayerMapUnlocked(Base):
    __tablename__ = "jugador_mapa_desbloqueado"

    player_id = Column("id_jugador", Integer, ForeignKey("jugador.id_jugador"), primary_key=True)
    map_id = Column("id_mapa", Integer, ForeignKey("mapa.id_mapa"), primary_key=True)
    unlocked_at = Column("fecha_desbloqueo", DateTime(timezone=False), nullable=True)

    player = relationship("Player", back_populates="unlocked_maps")
    game_map = relationship("Map", back_populates="unlocked_by_players")


class MapNpc(Base):
    __tablename__ = "mapa_npc"

    map_id = Column("id_mapa", Integer, ForeignKey("mapa.id_mapa"), primary_key=True)
    npc_id = Column("id_npc", Integer, ForeignKey("npc.id_npc"), primary_key=True)

    game_map = relationship("Map", back_populates="npc_links")
    npc = relationship("Npc", back_populates="map_links")


class MapItem(Base):
    __tablename__ = "mapa_item"

    map_id = Column("id_mapa", Integer, ForeignKey("mapa.id_mapa"), primary_key=True)
    item_id = Column("id_item", Integer, ForeignKey("item.id_item"), primary_key=True)
    # En la BD actual no existe quantity_available; usamos un valor por defecto en runtime.
    quantity_available = column_property(literal(1))

    game_map = relationship("Map", back_populates="item_links")
    item = relationship("Item", back_populates="map_links")
