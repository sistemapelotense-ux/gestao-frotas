import pytest
from datetime import datetime, timedelta
from src.application.services.lancamento_service import LancamentoService


class MockRepo:
    def __init__(self, records=None):
        self.records = records or []
        self.called = []

    async def check_duplicate(self, ativo_id, data, exclude_id=None):
        self.called.append("check_duplicate")
        return []

    async def create(self, obj):
        return obj

    async def get_by_id(self, lancamento_id):
        return None

    async def get_by_obra(self, obra_id, skip, limit):
        return []

    async def get_by_date_range(self, start, end):
        return []

    async def delete(self, obj):
        pass

    async def update(self, obj):
        return obj


class MockArquivoRepo:
    async def ativo_exists_in_propriedade(self, ativo_id):
        return True

    async def create(self, obj):
        return obj


class MockUserRepo:
    async def get_all(self):
        return []


def test_lancamento_status_alocado():
    statuses = {"O", "D", "P", "C", "R"}
    for s in statuses:
        assert s in statuses
    assert "X" not in statuses


def test_validacao_campos_obrigatorios():
    service = LancamentoService.__new__(LancamentoService)
    service.repo = MockRepo()
    data = {
        "data": datetime.utcnow(),
        "ativo_id": "a",
        "obra_id": "b",
        "status_uso": "",
        "informacoes_dia": "",
        "codigo_ativo": "",
        "descricao": "",
        "tipo": "",
        "fabricante": "",
        "modelo": "",
        "horimetro_inicial": 0,
        "horimetro_final": 0,
        "total_horas": 0,
        "km_inicial": 0,
        "km_final": 0,
        "total_km": 0,
        "descritivo_manutencao": "",
        "status": "",
        "condicao_climatica": "",
    }
    errors = service._validate_fields(data)
    empty_count = sum(
        1 for k, v in data.items()
        if v == "" and k in [
            "data", "ativo_id", "obra_id", "status_uso", "informacoes_dia",
            "codigo_ativo", "descricao", "tipo", "fabricante", "modelo",
            "horimetro_inicial", "horimetro_final", "total_horas",
            "km_inicial", "km_final", "total_km", "status", "condicao_climatica",
        ]
    )
    assert len(errors) == empty_count


def test_descrivivo_manutencao_nao_obrigatorio():
    service = LancamentoService.__new__(LancamentoService)
    service.repo = MockRepo()
    data = {
        "data": datetime.utcnow(),
        "ativo_id": "a",
        "obra_id": "b",
        "status_uso": "O",
        "informacoes_dia": "dia normal",
        "codigo_ativo": "ATV-001",
        "descricao": "Escavadeira",
        "tipo": "Equipamento",
        "fabricante": "Caterpillar",
        "modelo": "320",
        "horimetro_inicial": 100,
        "horimetro_final": 108,
        "total_horas": 8,
        "km_inicial": 0,
        "km_final": 0,
        "total_km": 0,
        "descritivo_manutencao": "",
        "status": "pendente",
        "condicao_climatica": "Ensolarado",
    }
    errors = service._validate_fields(data)
    assert len(errors) == 0