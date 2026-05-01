from pydantic import BaseModel


class CreatePaymentIntentIn(BaseModel):
    user_id: int
    pack_id: str
