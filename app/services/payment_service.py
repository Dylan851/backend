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


def _validate_purchase_context(db: Session, *, auth_player_id: int, user_id: int, pack_id: str):
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
    return pack


def create_payment_intent(db: Session, *, auth_player_id: int, user_id: int, pack_id: str):
    pack = _validate_purchase_context(db, auth_player_id=auth_player_id, user_id=user_id, pack_id=pack_id)

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


def create_checkout_session(
    db: Session,
    *,
    auth_player_id: int,
    user_id: int,
    pack_id: str,
    success_url: str | None = None,
    cancel_url: str | None = None,
):
    pack = _validate_purchase_context(db, auth_player_id=auth_player_id, user_id=user_id, pack_id=pack_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    frontend_base = settings.FRONTEND_URL.rstrip("/")
    final_success_url = success_url or f"{frontend_base}/#/payments?result=success"
    final_cancel_url = cancel_url or f"{frontend_base}/#/payments?result=cancel"

    session = stripe.checkout.Session.create(
        mode="payment",
        success_url=final_success_url,
        cancel_url=final_cancel_url,
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": pack_id},
                    "unit_amount": pack["amount"],
                },
                "quantity": 1,
            }
        ],
        metadata={
            "user_id": str(user_id),
            "pack_id": pack_id,
            "currency_type": pack["currency_type"],
            "quantity": str(pack["quantity"]),
        },
        payment_intent_data={
            "metadata": {
                "user_id": str(user_id),
                "pack_id": pack_id,
                "currency_type": pack["currency_type"],
                "quantity": str(pack["quantity"]),
            }
        },
    )
    return {"checkout_url": session.url, "checkout_session_id": session.id}


def _apply_successful_purchase(
    db: Session,
    *,
    payment_intent_id: str,
    metadata: dict,
    amount: int,
    currency: str,
):
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
        amount=amount,
        currency=currency,
        status="succeeded",
    )
    db.add(purchase)

    if currency_type == "coins":
        player.coins += quantity
    else:
        player.gems += quantity

    db.commit()


def handle_payment_intent_succeeded(db: Session, payment_intent):
    metadata = payment_intent.get("metadata", {}) or {}
    payment_intent_id = payment_intent.get("id", "")
    amount = int(payment_intent.get("amount_received") or payment_intent.get("amount") or 0)
    currency = str(payment_intent.get("currency", "eur"))
    _apply_successful_purchase(
        db,
        payment_intent_id=payment_intent_id,
        metadata=metadata,
        amount=amount,
        currency=currency,
    )


def handle_checkout_session_completed(db: Session, checkout_session):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    metadata = checkout_session.get("metadata", {}) or {}
    payment_intent_id = checkout_session.get("payment_intent", "")
    amount = int(checkout_session.get("amount_total") or 0)
    currency = str(checkout_session.get("currency", "eur"))

    if not payment_intent_id:
        return

    if not metadata:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        metadata = intent.get("metadata", {}) or {}
        amount = int(intent.get("amount_received") or intent.get("amount") or amount)
        currency = str(intent.get("currency", currency))

    _apply_successful_purchase(
        db,
        payment_intent_id=str(payment_intent_id),
        metadata=metadata,
        amount=amount,
        currency=currency,
    )
