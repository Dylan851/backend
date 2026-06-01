from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.enemy_repository import EnemyRepository


def get_enemy_by_id(db: Session, enemy_id: int):
    """Obtiene un Enemigo por ID"""
    enemy = EnemyRepository.get_by_id(db, enemy_id)
    if not enemy:
        raise HTTPException(status_code=404, detail="Enemy not found")
    return enemy


def get_enemies_by_map(db: Session, map_id: int):
    """Obtiene todos los Enemigos de un mapa"""
    return EnemyRepository.get_by_map(db, map_id)


def get_enemies_by_level(db: Session, nivel: int):
    """Obtiene todos los Enemigos de un nivel específico"""
    return EnemyRepository.get_by_level(db, nivel)


def build_enemy_response(enemy):
    """Construye la respuesta de un Enemigo"""
    npc_name = enemy.npc.name if enemy.npc else "Unknown"
    return {
        "id": enemy.id_npc,
        "name": npc_name,
        "nivel": enemy.nivel,
        "dano": enemy.dano,
    }


def build_enemy_list(enemies):
    """Construye una lista de respuestas de Enemigos"""
    return [build_enemy_response(enemy) for enemy in enemies]


def calculate_experience_gained(player_level: int, enemy_level: int, defeated: bool = True):
    """
    Calcula la experiencia ganada al derrotar un enemigo
    Fórmula: (enemyLevel - playerLevel + 10) * 10, mínimo 50
    """
    if not defeated:
        return 0
    base_exp = max(50, (enemy_level - player_level + 10) * 10)
    return base_exp


def calculate_damage_taken(enemy_dano: int, player_defense: int = 0):
    """
    Calcula el daño tomado en combate
    Formula simplificada: damage = enemy_dano - (player_defense // 4)
    """
    damage = max(1, enemy_dano - (player_defense // 4))
    return damage
