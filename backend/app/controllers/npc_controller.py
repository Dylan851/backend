from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.services import npc_service


def get_npcs_by_map(
    map_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene todos los NPCs de un mapa"""
    npcs = npc_service.get_npcs_by_map(db, map_id)
    return {
        "success": True,
        "data": {
            "npcs": npc_service.build_npc_list(npcs),
            "total": len(npcs),
        },
    }


def get_npc_detail(
    npc_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene los detalles de un NPC específico"""
    npc = npc_service.get_npc_by_id(db, npc_id)
    return {
        "success": True,
        "data": npc_service.build_npc_response(npc),
    }
