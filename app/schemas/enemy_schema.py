from pydantic import BaseModel, Field


class EnemyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    nivel: int = Field(default=1, ge=1, le=100)
    dano: int = Field(default=10, ge=1, le=1000)


class EnemyCreate(EnemyBase):
    pass


class EnemyResponse(EnemyBase):
    id: int = Field(alias="id_npc")

    class Config:
        from_attributes = True
        populate_by_name = True


class DefeatEnemyResponse(BaseModel):
    enemy_id: int
    experience_gained: int
    message: str
