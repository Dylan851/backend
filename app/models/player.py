from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class Player(Base):
    __tablename__ = "Jugador"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Usuario.id"), unique=True, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    coins = Column(Integer, default=0, nullable=False)
    coord_lat = Column(Float, default=0.0, nullable=False)
    coord_lng = Column(Float, default=0.0, nullable=False)
    current_map_id = Column(Integer, ForeignKey("Mapa.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="player")
    inventory = relationship("PlayerItem", back_populates="player")
    captures = relationship("Capture", back_populates="player")
    unlocked_maps = relationship("PlayerMapUnlocked", back_populates="player")
    purchases = relationship("Purchase", back_populates="player")
    coin_transactions = relationship("CoinTransaction", back_populates="player")
