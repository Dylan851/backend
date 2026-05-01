from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.config.settings import settings
from app.middleware.auth_middleware import get_current_player
from app.schemas.payment_schema import CreatePaymentIntentIn
from app.services import payment_service

import stripe


def create_payment_intent(
    payload: CreatePaymentIntentIn,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    result = payment_service.create_payment_intent(
        db,
        auth_player_id=player.id,
        user_id=payload.user_id,
        pack_id=payload.pack_id,
    )
    return {"success": True, "data": result}


async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET.strip()
    if not webhook_secret:
        raise HTTPException(status_code=503, detail="STRIPE_WEBHOOK_SECRET is not configured")

    signature = request.headers.get("Stripe-Signature")
    if not signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")

    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=signature, secret=webhook_secret)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid payload: {exc}") from exc
    except stripe.error.SignatureVerificationError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid signature: {exc}") from exc

    if event["type"] == "payment_intent.succeeded":
        payment_service.handle_payment_intent_succeeded(db, event["data"]["object"])

    return {"received": True}
