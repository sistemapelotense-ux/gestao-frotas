from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.lancamento_repository import LancamentoRepository
from src.infrastructure.repositories.arquivo_propriedade_repository import ArquivoPropriedadeRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.database.models import LancamentoDiarioModel, UserModel
from src.infrastructure.database.models import AtivoModel, ObraModel
import uuid

LOCACAO_STATUSES = {"O", "D", "P", "C", "R"}


class LancamentoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = LancamentoRepository(db)
        self.arquivo_repo = ArquivoPropriedadeRepository(db)
        self.user_repo = UserRepository(db)

    async def create(self, data: dict, usuario: UserModel) -> LancamentoDiarioModel:
        errors = self._validate_fields(data)
        if errors:
            raise ValueError("; ".join(errors))

        ativo_id = data["ativo_id"]
        obra_id = data["obra_id"]
        lancamento_data = data["data"]

        if usuario.papel == "obra" and usuario.obra_id != obra_id:
            raise ValueError("Usuário de obra só pode registrar na sua própria obra")

        duplicatas = await self.repo.check_duplicate(ativo_id, lancamento_data)
        if duplicatas:
            raise ValueError("Este ativo já possui lançamento nesta data. Detectada duplicidade.")

        data["total_horas"] = data.get("horimetro_final", 0) - data.get("horimetro_inicial", 0)
        data["total_km"] = data.get("km_final", 0) - data.get("km_inicial", 0)
        data["usuario_id"] = usuario.id

        lancamento = LancamentoDiarioModel(**data)
        result = await self.repo.create(lancamento)
        await self._auto_incluir_propriedade(ativo_id)
        return result

    async def update(self, lancamento_id: uuid.UUID, data: dict, usuario: UserModel) -> LancamentoDiarioModel:
        errors = self._validate_fields(data)
        if errors:
            raise ValueError("; ".join(errors))

        lancamento = await self.repo.get_by_id(lancamento_id)
        if lancamento is None:
            raise ValueError("Lançamento não encontrado")

        if usuario.papel == "obra" and lancamento.usuario_id != usuario.id:
            raise ValueError("Usuário de obra só pode editar seus próprios registros")

        data["total_horas"] = data.get("horimetro_final", 0) - data.get("horimetro_inicial", 0)
        data["total_km"] = data.get("km_final", 0) - data.get("km_inicial", 0)

        for key, value in data.items():
            if value is not None and hasattr(lancamento, key):
                setattr(lancamento, key, value)

        return await self.repo.update(lancamento)

    async def get_by_id(self, lancamento_id: uuid.UUID) -> LancamentoDiarioModel:
        lancamento = await self.repo.get_by_id(lancamento_id)
        if lancamento is None:
            raise ValueError("Lançamento não encontrado")
        return lancamento

    async def get_by_usuario(self, usuario: UserModel, skip: int = 0, limit: int = 100) -> list[LancamentoDiarioModel]:
        if usuario.papel == "obra":
            return await self.repo.get_by_obra(usuario.obra_id, skip, limit)
        return await self.repo.get_all(skip, limit)

    async def delete(self, lancamento_id: uuid.UUID, usuario: UserModel) -> None:
        lancamento = await self.repo.get_by_id(lancamento_id)
        if lancamento is None:
            raise ValueError("Lançamento não encontrado")
        if usuario.papel == "obra" and lancamento.usuario_id != usuario.id:
            raise ValueError("Usuário de obra só pode excluir seus próprios registros")
        await self.repo.delete(lancamento)

    async def get_duplicates_for_date(self, data: datetime) -> list[dict]:
        day_start = data.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = data.replace(hour=23, minute=59, second=59, microsecond=999999)
        lancamentos = await self.repo.get_by_date_range(day_start, day_end)
        ativo_obras: dict[str, list] = {}
        for l in lancamentos:
            key = str(l.ativo_id)
            ativo_obras.setdefault(key, []).append(l)
        duplicates = []
        for ativo_id, items in ativo_obras.items():
            if len(set(str(i.obra_id) for i in items)) > 1:
                duplicates.append({"ativo_id": ativo_id, "lancamentos": items})
        return duplicates

    async def _auto_incluir_propriedade(self, ativo_id: uuid.UUID) -> None:
        if not await self.arquivo_repo.ativo_exists_in_propriedade(ativo_id):
            from src.infrastructure.database.models import ArquivoPropriedadeModel
            prop = ArquivoPropriedadeModel(ativo_id=ativo_id, status="L")
            await self.arquivo_repo.create(prop)

    def _validate_fields(self, data: dict) -> list[str]:
        required = [
            "data", "ativo_id", "obra_id", "status_uso", "informacoes_dia",
            "codigo_ativo", "descricao", "tipo", "fabricante", "modelo",
            "horimetro_inicial", "horimetro_final", "total_horas",
            "km_inicial", "km_final", "total_km", "status", "condicao_climatica",
        ]
        errors = []
        for field in required:
            val = data.get(field)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                errors.append(f"Campo '{field}' é obrigatório")
        return errors
