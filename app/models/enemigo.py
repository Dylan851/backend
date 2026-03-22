from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Enemigo(Base):
    """
    Modelo para Enemigos (hereda de NPC)
    ISA: Enemigo es una especialización de NPC
    """
    __tablename__ = "Enemigo"

    id_npc = Column(Integer, ForeignKey("NPC.id"), primary_key=True)
    nivel = Column(Integer, default=1, nullable=False)
    dano = Column(Integer, default=10, nullable=False)
    
    # Relación con NPC
    npc = relationship("Npc", foreign_keys=[id_npc], uselist=False, lazy="joined")

    __mapper_args__ = {
        "primary_join": "Enemigo.id_npc == Npc.id",
    }
