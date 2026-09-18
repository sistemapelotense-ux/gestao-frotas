from pydantic import BaseModel
import uuid
from datetime import datetime


class ArquivoPropriedadeCreate(BaseModel):
    ativo_id: uuid.UUID
    status: str = "P"


class ArquivoPropriedadeUpdate(BaseModel):
    status: str | None = None


class ArquivoPropriedadeResponse(BaseModel):
    id: uuid.UUID
    ativo_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
