from pydantic import BaseModel
import uuid
from datetime import datetime


class ObraCreate(BaseModel):
    nome: str
    localizacao: str


class ObraUpdate(BaseModel):
    nome: str | None = None
    localizacao: str | None = None
    ativa: bool | None = None


class ObraResponse(BaseModel):
    id: uuid.UUID
    nome: str
    localizacao: str
    ativa: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
