from pydantic import BaseModel, EmailStr
import uuid
from datetime import datetime


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str
    nome: str
    papel: str = "obra"
    obra_id: uuid.UUID | None = None


class UsuarioUpdate(BaseModel):
    email: EmailStr | None = None
    nome: str | None = None
    papel: str | None = None
    obra_id: uuid.UUID | None = None
    ativo: bool | None = None
    password: str | None = None


class UsuarioResponse(BaseModel):
    id: uuid.UUID
    email: str
    nome: str
    papel: str
    obra_id: uuid.UUID | None
    ativo: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
