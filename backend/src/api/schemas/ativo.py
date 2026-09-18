from pydantic import BaseModel
import uuid
from datetime import datetime


class AtivoCreate(BaseModel):
    identificacao: str
    descricao: str = ""
    tipo: str = ""
    fabricante: str = ""
    modelo: str = ""


class AtivoUpdate(BaseModel):
    identificacao: str | None = None
    descricao: str | None = None
    tipo: str | None = None
    fabricante: str | None = None
    modelo: str | None = None
    status: str | None = None


class AtivoResponse(BaseModel):
    id: uuid.UUID
    identificacao: str
    descricao: str
    tipo: str
    fabricante: str
    modelo: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
