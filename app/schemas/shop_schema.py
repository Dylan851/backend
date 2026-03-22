from pydantic import BaseModel


class ItemOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: int

    class Config:
        from_attributes = True


class PurchaseIn(BaseModel):
    item_id: int
