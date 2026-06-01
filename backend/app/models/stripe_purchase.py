from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.sql import func

from app.config.database import Base


class StripePurchase(Base):
    __tablename__ = "stripe_purchase"
    __table_args__ = (UniqueConstraint("payment_intent_id", name="uq_stripe_purchase_payment_intent_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    payment_intent_id = Column(String(255), nullable=False)
    pack_id = Column(String(64), nullable=False)
    currency_type = Column(String(32), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String(10), nullable=False)
    status = Column(String(32), nullable=False, default="succeeded")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
