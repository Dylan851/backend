from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.config.database import Base


class Npc(Base):
    __tablename__ = "NPC"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    role = Column(String(100), nullable=True)

    map_links = relationship("MapNpc", back_populates="npc")
