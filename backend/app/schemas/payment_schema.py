from pydantic import BaseModel


class CreatePaymentIntentIn(BaseModel):
    user_id: int
    pack_id: str


class CreateCheckoutSessionIn(BaseModel):
    user_id: int
    pack_id: str
    success_url: str | None = None
    cancel_url: str | None = None
