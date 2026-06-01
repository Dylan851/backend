from sqlalchemy.orm import Session

from app.models.item import Item, PlayerItem
from app.models.purchase import Purchase, CoinTransaction
from app.models.player import Player


def list_items(db: Session):
    return db.query(Item).all()


def get_item(db: Session, item_id: int) -> Item | None:
    return db.query(Item).filter(Item.id == item_id).first()


def add_item_to_inventory(db: Session, player_id: int, item_id: int, quantity: int = 1):
    player_item = (
        db.query(PlayerItem)
        .filter(PlayerItem.player_id == player_id, PlayerItem.item_id == item_id)
        .first()
    )
    if player_item:
        player_item.quantity += quantity
    else:
        player_item = PlayerItem(player_id=player_id, item_id=item_id, quantity=quantity)
        db.add(player_item)
    return player_item


def create_purchase(db: Session, player_id: int, item_id: int, price: int) -> Purchase:
    purchase = Purchase(player_id=player_id, item_id=item_id, price=price)
    db.add(purchase)
    return purchase


def update_player_coins(db: Session, player: Player, delta: int, reason: str | None = None):
    player.coins += delta
    tx = CoinTransaction(player_id=player.id, delta=delta, reason=reason)
    db.add(tx)
    return tx
