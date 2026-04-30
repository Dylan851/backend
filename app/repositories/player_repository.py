from sqlalchemy.orm import Session

from app.models.item import Item, PlayerItem
from app.models.animal import Animal, Capture
from app.models.map import Map, PlayerMapUnlocked
from app.models.player import Player
from app.models.user import User


def create_player(db: Session, nickname: str | None = None) -> Player:
    player = Player(nickname=nickname, level=1, coins=0, coord_lat=0.0, coord_lng=0.0)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def get_by_user_id(db: Session, user_id: int) -> Player | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.player_id:
        return None
    return db.query(Player).filter(Player.id == user.player_id).first()


def get_by_id(db: Session, player_id: int) -> Player | None:
    return db.query(Player).filter(Player.id == player_id).first()


def update_location(db: Session, player: Player, coord_lat: float, coord_lng: float) -> Player:
    player.coord_lat = coord_lat
    player.coord_lng = coord_lng
    db.commit()
    db.refresh(player)
    return player


def update_profile(
    db: Session,
    player: Player,
    *,
    nickname: str | None = None,
    coins: int | None = None,
    gems: int | None = None,
) -> Player:
    if nickname is not None:
        player.nickname = nickname
    if coins is not None:
        player.coins = max(0, coins)
    if gems is not None:
        player.gems = max(0, gems)
    db.commit()
    db.refresh(player)
    return player


def get_inventory(db: Session, player_id: int):
    rows = (
        db.query(PlayerItem, Item)
        .join(Item, PlayerItem.item_id == Item.id)
        .filter(PlayerItem.player_id == player_id)
        .all()
    )
    return [
        {
            "item_id": item.id,
            "name": item.name,
            "quantity": player_item.quantity,
        }
        for player_item, item in rows
    ]


def get_captured_animals(db: Session, player_id: int):
    rows = (
        db.query(Capture, Animal)
        .join(Animal, Capture.animal_id == Animal.id)
        .filter(Capture.player_id == player_id)
        .all()
    )
    return [
        {
            "id": animal.id,
            "name": animal.name,
            "rarity": animal.rarity,
            "captured_at": capture.captured_at,
        }
        for capture, animal in rows
    ]


def get_unlocked_maps(db: Session, player_id: int):
    rows = (
        db.query(PlayerMapUnlocked, Map)
        .join(Map, PlayerMapUnlocked.map_id == Map.id)
        .filter(PlayerMapUnlocked.player_id == player_id)
        .all()
    )
    return [
        {
            "id": game_map.id,
            "name": game_map.name,
            "required_level": game_map.required_level,
        }
        for unlocked, game_map in rows
    ]
