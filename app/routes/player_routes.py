from fastapi import APIRouter

from app.controllers import player_controller

router = APIRouter(prefix="/player", tags=["player"])

router.get("/profile")(player_controller.get_profile)
router.put("/location")(player_controller.update_location)
router.get("/inventory")(player_controller.get_inventory)
