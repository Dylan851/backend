from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.schemas.shop_schema import PurchaseIn
from app.services import shop_service


def list_shop(db: Session = Depends(get_db)):
    items = shop_service.list_items(db)
    payload = [
        {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
        }
        for item in items
    ]
    return {"success": True, "data": {"items": payload}}


def buy_item(
    payload: PurchaseIn,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    result = shop_service.buy_item(db, player.id, payload.item_id)
    return {"success": True, "data": result}
