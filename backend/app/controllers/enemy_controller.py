from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.middleware.auth_middleware import get_current_player
from app.services import enemy_service
from app.repositories import player_repository


def list_map_enemies(
    map_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene todos los Enemigos de un mapa"""
    enemies = enemy_service.get_enemies_by_map(db, map_id)
    return {
        "success": True,
        "data": {
            "enemies": enemy_service.build_enemy_list(enemies),
            "total": len(enemies),
        },
    }


def get_enemy_detail(
    enemy_id: int,
    db: Session = Depends(get_db),
):
    """Obtiene los detalles de un Enemigo específico"""
    enemy = enemy_service.get_enemy_by_id(db, enemy_id)
    return {
        "success": True,
        "data": enemy_service.build_enemy_response(enemy),
    }


def defeat_enemy(
    enemy_id: int,
    db: Session = Depends(get_db),
    player=Depends(get_current_player),
):
    """
    Registra la derrota de un enemigo
    Calcula la experiencia ganada y actualiza el jugador
    """
    enemy = enemy_service.get_enemy_by_id(db, enemy_id)

    # Calcular experiencia ganada
    exp_gained = enemy_service.calculate_experience_gained(
        player_level=player.level, enemy_level=enemy.nivel, defeated=True
    )

    # TODO: Implementar sistema de experiencia y niveles
    # Por ahora, solo retornamos la información

    return {
        "success": True,
        "data": {
            "enemy_id": enemy.id_npc,
            "experience_gained": exp_gained,
            "message": f"You defeated {enemy.npc.name} and gained {exp_gained} experience!",
        },
    }
