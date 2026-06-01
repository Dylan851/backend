from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, literal
from sqlalchemy.orm import relationship, column_property, synonym
from sqlalchemy.sql import func

from app.config.database import Base


class User(Base):
    __tablename__ = "usuario"

    id = Column("id_usuario", Integer, primary_key=True, index=True)
    email = Column("email", String(255), unique=True, index=True, nullable=False)
    password_hash = Column("password_hash", String(255), nullable=False)
    has_password = Column("has_password", Boolean, nullable=False, default=True)
    has_google = Column("has_google", Boolean, nullable=False, default=False)
    player_id = Column("id_jugador", Integer, ForeignKey("jugador.id_jugador"), nullable=True)
    # En la BD actual no existe username/created_at; usamos alias en runtime.
    username = synonym("email")
    created_at = column_property(literal(None))

    player = relationship("Player", back_populates="user", uselist=False)
