from pydantic import BaseModel
import uuid
from datetime import datetime


class LancamentoCreate(BaseModel):
    data: datetime
    ativo_id: uuid.UUID
    obra_id: uuid.UUID
    status_uso: str
    informacoes_dia: str
    codigo_ativo: str
    descricao: str
    tipo: str
    fabricante: str
    modelo: str
    horimetro_inicial: float
    horimetro_final: float
    total_horas: float = 0.0
    km_inicial: float
    km_final: float
    total_km: float = 0.0
    descritivo_manutencao: str = ""
    status: str
    condicao_climatica: str


class LancamentoUpdate(BaseModel):
    data: datetime | None = None
    ativo_id: uuid.UUID | None = None
    obra_id: uuid.UUID | None = None
    status_uso: str | None = None
    informacoes_dia: str | None = None
    codigo_ativo: str | None = None
    descricao: str | None = None
    tipo: str | None = None
    fabricante: str | None = None
    modelo: str | None = None
    horimetro_inicial: float | None = None
    horimetro_final: float | None = None
    total_horas: float | None = None
    km_inicial: float | None = None
    km_final: float | None = None
    total_km: float | None = None
    descritivo_manutencao: str | None = None
    status: str | None = None
    condicao_climatica: str | None = None


class LancamentoResponse(BaseModel):
    id: uuid.UUID
    data: datetime
    ativo_id: uuid.UUID
    obra_id: uuid.UUID
    usuario_id: uuid.UUID
    status_uso: str
    informacoes_dia: str
    codigo_ativo: str
    descricao: str
    tipo: str
    fabricante: str
    modelo: str
    horimetro_inicial: float
    horimetro_final: float
    total_horas: float
    km_inicial: float
    km_final: float
    total_km: float
    descritivo_manutencao: str | None
    status: str
    condicao_climatica: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
