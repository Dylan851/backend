from fastapi import APIRouter

from app.controllers import map_controller, npc_controller, enemy_controller

router = APIRouter(prefix="/maps", tags=["maps"])

router.get("")(map_controller.list_maps)
router.get("/unlocked")(map_controller.list_unlocked_maps)
router.post("/unlock")(map_controller.unlock_map)

npc_router = APIRouter(prefix="/npc", tags=["npc"])

npc_router.get("/map/{map_id}")(npc_controller.get_npcs_by_map)
npc_router.get("/{npc_id}")(npc_controller.get_npc_detail)

enemy_router = APIRouter(prefix="/enemies", tags=["enemies"])

enemy_router.get("/map/{map_id}")(enemy_controller.list_map_enemies)
enemy_router.get("/{enemy_id}")(enemy_controller.get_enemy_detail)
enemy_router.post("/{enemy_id}/defeat")(enemy_controller.defeat_enemy)
