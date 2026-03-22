from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.npc_repository import NpcRepository


def get_npc_by_id(db: Session, npc_id: int):
    """Obtiene un NPC por ID"""
    npc = NpcRepository.get_by_id(db, npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    return npc


def get_npcs_by_map(db: Session, map_id: int):
    """Obtiene todos los NPCs de un mapa"""
    return NpcRepository.get_by_map(db, map_id)


def build_npc_response(npc):
    """Construye la respuesta de un NPC"""
    return {
        "id": npc.id,
        "name": npc.name,
        "role": npc.role,
    }


def build_npc_list(npcs):
    """Construye una lista de respuestas de NPCs"""
    return [build_npc_response(npc) for npc in npcs]
