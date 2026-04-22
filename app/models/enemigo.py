from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base


class Enemigo(Base):
    """
    Modelo para Enemigos (hereda de NPC)
    ISA: Enemigo es una especialización de NPC
    """
    __tablename__ = "enemigo"

    id_npc = Column("id_npc", Integer, ForeignKey("npc.id_npc"), primary_key=True)
    nivel = Column(Integer, default=1, nullable=False)
    dano = Column(Integer, default=10, nullable=False)
    
    # Relación con NPC
    npc = relationship("Npc", foreign_keys=[id_npc], uselist=False, lazy="joined")

    # Nota: no usamos __mapper_args__ aquí; la relación con Npc se resuelve por FK.
