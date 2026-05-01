from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config.settings import settings
from app.models.player import Player
from app.models.stripe_purchase import StripePurchase

import stripe

PACKS = {
    "coins_100": {"quantity": 100, "amount": 99, "currency_type": "coins"},
    "coins_500": {"quantity": 500, "amount": 299, "currency_type": "coins"},
    "coins_1000": {"quantity": 1000, "amount": 499, "currency_type": "coins"},
    "diamonds_10": {"quantity": 10, "amount": 199, "currency_type": "diamonds"},
    "diamonds_30": {"quantity": 30, "amount": 499, "currency_type": "diamonds"},
    "diamonds_75": {"quantity": 75, "amount": 999, "currency_type": "diamonds"},
}


def _stripe_configured() -> bool:
    return settings.STRIPE_SECRET_KEY.strip() != ""


def create_payment_intent(db: Session, *, auth_player_id: int, user_id: int, pack_id: str):
    if not _stripe_configured():
        raise HTTPException(status_code=500, detail="Stripe is not configured on the server")
    if auth_player_id != user_id:
        raise HTTPException(status_code=403, detail="user_id does not match authenticated user")
    pack = PACKS.get(pack_id)
    if not pack:
        raise HTTPException(status_code=400, detail="Invalid pack_id")
    player = db.query(Player).filter(Player.id == user_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    payment_intent = stripe.PaymentIntent.create(
        amount=pack["amount"],
        currency="eur",
        metadata={
            "user_id": str(user_id),
            "pack_id": pack_id,
            "currency_type": pack["currency_type"],
            "quantity": str(pack["quantity"]),
        },
        automatic_payment_methods={"enabled": True},
    )
    return {
        "client_secret": payment_intent.client_secret,
        "payment_intent_id": payment_intent.id,
    }


def handle_payment_intent_succeeded(db: Session, payment_intent):
    metadata = payment_intent.get("metadata", {}) or {}
    payment_intent_id = payment_intent.get("id", "")
    if not payment_intent_id:
        return

    exists = (
        db.query(StripePurchase)
        .filter(StripePurchase.payment_intent_id == payment_intent_id)
        .first()
    )
    if exists:
        return

    user_id = int(metadata.get("user_id", "0"))
    pack_id = str(metadata.get("pack_id", ""))
    currency_type = str(metadata.get("currency_type", ""))
    quantity = int(metadata.get("quantity", "0"))

    if user_id <= 0 or quantity <= 0 or currency_type not in {"coins", "diamonds"} or not pack_id:
        raise HTTPException(status_code=400, detail="Invalid payment metadata")

    player = db.query(Player).filter(Player.id == user_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found for payment")

    purchase = StripePurchase(
        user_id=user_id,
        payment_intent_id=payment_intent_id,
        pack_id=pack_id,
        currency_type=currency_type,
        quantity=quantity,
        amount=int(payment_intent.get("amount_received") or payment_intent.get("amount") or 0),
        currency=str(payment_intent.get("currency", "eur")),
        status="succeeded",
    )
    db.add(purchase)

    if currency_type == "coins":
        player.coins += quantity
    else:
        player.gems += quantity

    db.commit()
