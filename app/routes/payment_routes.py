from fastapi import APIRouter

from app.controllers import payment_controller

router = APIRouter(tags=["payments"])

router.post("/payments/create-payment-intent")(payment_controller.create_payment_intent)
router.post("/stripe/webhook")(payment_controller.stripe_webhook)
