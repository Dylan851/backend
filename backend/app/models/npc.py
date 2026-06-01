from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class Npc(Base):
    __tablename__ = "npc"

    id = Column("id_npc", Integer, primary_key=True, index=True)
    name = Column("nombre", String(150), nullable=False)
    role = Column("habilidad", String(100), nullable=True)

    map_links = relationship("MapNpc", back_populates="npc")
