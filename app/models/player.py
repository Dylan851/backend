from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, literal
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from app.config.database import Base


class Player(Base):
    __tablename__ = "jugador"

    id = Column("id_jugador", Integer, primary_key=True, index=True)
    nickname = Column("apodo", String(150), nullable=True)
    level = Column("nivel", Integer, default=1, nullable=False)
    coins = Column("monedas", Integer, default=0, nullable=False)
    coord_lat = Column("ultima_latitud", Float, default=0.0, nullable=False)
    coord_lng = Column("ultima_longitud", Float, default=0.0, nullable=False)
    # En la BD actual no existe current_map_id; usamos None en runtime.
    current_map_id = column_property(literal(None))
    updated_at = column_property(literal(None))

    user = relationship("User", back_populates="player", uselist=False)
    inventory = relationship("PlayerItem", back_populates="player")
    captures = relationship("Capture", back_populates="player")
    unlocked_maps = relationship("PlayerMapUnlocked", back_populates="player")
    purchases = relationship("Purchase", back_populates="player")
    coin_transactions = relationship("CoinTransaction", back_populates="player")
