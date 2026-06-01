from pydantic import BaseModel, Field


class NpcBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    role: str = Field(None, max_length=100)


class NpcCreate(NpcBase):
    pass


class NpcResponse(NpcBase):
    id: int

    class Config:
        from_attributes = True
