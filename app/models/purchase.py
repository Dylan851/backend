from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class Purchase(Base):
    __tablename__ = "Compra"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("Jugador.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("Item.id"), nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("Player", back_populates="purchases")
    item = relationship("Item")


class CoinTransaction(Base):
    __tablename__ = "Transaccion_Monedas"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("Jugador.id"), nullable=False)
    delta = Column(Integer, nullable=False)
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship("Player", back_populates="coin_transactions")
