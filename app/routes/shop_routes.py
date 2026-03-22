from fastapi import APIRouter

from app.controllers import shop_controller

router = APIRouter(prefix="/shop", tags=["shop"])

router.get("")(shop_controller.list_shop)
router.post("/buy")(shop_controller.buy_item)
