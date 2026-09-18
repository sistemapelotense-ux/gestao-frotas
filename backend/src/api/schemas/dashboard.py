from pydantic import BaseModel


class DashboardResumo(BaseModel):
    total_ativos: int
    total_obras: int
    lancamentos_hoje: int
    ativos_alocados_hoje: int
    ativos_nao_alocados: int
    duplicidades_hoje: int
    detalhe_nao_alocados: list[dict]
    detalhe_duplicidades: list[dict]


class DashboardLancamento(BaseModel):
    id: str
    data: str
    ativo: str
    obra: str
    status_uso: str
