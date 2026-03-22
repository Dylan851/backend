from typing import Optional

from pydantic import BaseModel


class AnimalOut(BaseModel):
    id: int
    name: str
    rarity: Optional[str]

    class Config:
        from_attributes = True


class CaptureIn(BaseModel):
    animal_id: int
