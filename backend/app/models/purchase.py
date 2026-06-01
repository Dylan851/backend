from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, literal
from sqlalchemy.orm import relationship, column_property
from sqlalchemy.sql import func

from app.config.database import Base


class Purchase(Base):
    __tablename__ = "compra"

    id = Column("id_compra", Integer, primary_key=True, index=True)
    player_id = Column("id_jugador", Integer, ForeignKey("jugador.id_jugador"), nullable=False)
    # En la BD actual el item de tienda es id_tienda_item
    item_id = Column("id_tienda_item", Integer, nullable=False)
    price = column_property(literal(0))
    created_at = Column("fecha", DateTime(timezone=False), nullable=True)

    player = relationship("Player", back_populates="purchases")


class CoinTransaction(Base):
    __tablename__ = "transaccion_monedas"

    id = Column("id_transaccion", Integer, primary_key=True, index=True)
    player_id = Column("id_jugador", Integer, ForeignKey("jugador.id_jugador"), nullable=False)
    delta = Column("cantidad", Integer, nullable=False)
    reason = Column("motivo", String(255), nullable=True)
    created_at = Column("fecha", DateTime(timezone=False), nullable=True)

    player = relationship("Player", back_populates="coin_transactions")
