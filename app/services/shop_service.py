from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import player_repository, shop_repository


def list_items(db: Session):
    return shop_repository.list_items(db)


def buy_item(db: Session, player_id: int, item_id: int):
    player = player_repository.get_by_id(db, player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    item = shop_repository.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if player.coins < item.price:
        raise HTTPException(status_code=400, detail="Not enough coins")

    shop_repository.update_player_coins(db, player, -item.price, reason="shop_purchase")
    shop_repository.create_purchase(db, player.id, item.id, item.price)
    shop_repository.add_item_to_inventory(db, player.id, item.id, quantity=1)

    db.commit()
    db.refresh(player)

    return {
        "player_id": player.id,
        "item_id": item.id,
        "remaining_coins": player.coins,
    }
