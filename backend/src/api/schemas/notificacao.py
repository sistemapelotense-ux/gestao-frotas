from pydantic import BaseModel
import uuid
from datetime import datetime


class NotificacaoResponse(BaseModel):
    id: uuid.UUID
    titulo: str
    mensagem: str
    lida: bool
    tipo: str
    created_at: datetime

    class Config:
        from_attributes = True


class NotificacaoCountResponse(BaseModel):
    nao_lidas: int
