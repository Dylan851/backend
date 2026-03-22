from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Aldeano(Base):
    """
    Modelo para Aldeanos (hereda de NPC)
    ISA: Aldeano es una especialización de NPC
    """
    __tablename__ = "Aldeano"

    id_npc = Column(Integer, ForeignKey("NPC.id"), primary_key=True)
    
    # Relación con NPC
    npc = relationship("Npc", foreign_keys=[id_npc], uselist=False, lazy="joined")

    __mapper_args__ = {
        "primary_join": "Aldeano.id_npc == Npc.id",
    }
