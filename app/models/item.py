from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class Item(Base):
    __tablename__ = "Item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, default=0, nullable=False)

    player_items = relationship("PlayerItem", back_populates="item")
    map_links = relationship("MapItem", back_populates="item")


class PlayerItem(Base):
    __tablename__ = "Jugador_Item"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("Jugador.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)

    player = relationship("Player", back_populates="inventory")
    item = relationship("Item", back_populates="player_items")
