from sqlalchemy import Column, ForeignKey, Integer, String, literal
from sqlalchemy.orm import relationship, column_property

from app.config.database import Base


class Item(Base):
    __tablename__ = "item"

    id = Column("id_item", Integer, primary_key=True, index=True)
    name = Column("nombre", String(150), nullable=False)
    item_type = Column("tipo", String(100), nullable=True)
    # En la BD actual no existen estos campos:
    description = column_property(literal(None))
    price = column_property(literal(0))

    player_items = relationship("PlayerItem", back_populates="item")
    map_links = relationship("MapItem", back_populates="item")


class PlayerItem(Base):
    __tablename__ = "jugador_item"

    player_id = Column("id_jugador", Integer, ForeignKey("jugador.id_jugador"), primary_key=True)
    item_id = Column("id_item", Integer, ForeignKey("item.id_item"), primary_key=True)
    # En la BD actual no existe quantity; usamos 1 por defecto.
    quantity = column_property(literal(1))

    player = relationship("Player", back_populates="inventory")
    item = relationship("Item", back_populates="player_items")
