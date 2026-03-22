from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PlayerLocationUpdate(BaseModel):
    coord_lat: float
    coord_lng: float


class MapOut(BaseModel):
    id: int
    name: str
    required_level: int

    class Config:
        from_attributes = True


class InventoryItemOut(BaseModel):
    item_id: int
    name: str
    quantity: int


class CapturedAnimalOut(BaseModel):
    id: int
    name: str
    rarity: Optional[str]
    captured_at: datetime


class PlayerProfileOut(BaseModel):
    id: int
    level: int
    coins: int
    coord_lat: float
    coord_lng: float
    current_map_id: Optional[int]
    inventory: List[InventoryItemOut]
    captured_animals: List[CapturedAnimalOut]
    unlocked_maps: List[MapOut]

    class Config:
        from_attributes = True
