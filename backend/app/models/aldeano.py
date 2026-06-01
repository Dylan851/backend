from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Aldeano(Base):
    """
    Modelo para Aldeanos (hereda de NPC)
    ISA: Aldeano es una especialización de NPC
    """
    __tablename__ = "aldeano"

    id_npc = Column("id_npc", Integer, ForeignKey("npc.id_npc"), primary_key=True)
    
    # Relación con NPC
    npc = relationship("Npc", foreign_keys=[id_npc], uselist=False, lazy="joined")

    # Nota: no usamos __mapper_args__ aquí; la relación con Npc se resuelve por FK.
