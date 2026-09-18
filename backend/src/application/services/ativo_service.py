from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.ativo_repository import AtivoRepository
from src.infrastructure.database.models import AtivoModel
import uuid


class AtivoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AtivoRepository(db)

    async def create(self, identificacao: str, descricao: str, tipo: str, fabricante: str, modelo: str) -> AtivoModel:
        if await self.repo.identificacao_exists(identificacao):
            raise ValueError("Já existe um ativo com essa identificação")
        ativo = AtivoModel(
            identificacao=identificacao,
            descricao=descricao,
            tipo=tipo,
            fabricante=fabricante,
            modelo=modelo,
            status="disponivel",
        )
        return await self.repo.create(ativo)

    async def get_by_id(self, ativo_id: uuid.UUID) -> AtivoModel:
        ativo = await self.repo.get_by_id(ativo_id)
        if ativo is None:
            raise ValueError("Ativo não encontrado")
        return ativo

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[AtivoModel]:
        return await self.repo.get_all(skip, limit)

    async def update(self, ativo_id: uuid.UUID, **kwargs) -> AtivoModel:
        ativo = await self.get_by_id(ativo_id)
        if "identificacao" in kwargs and kwargs["identificacao"] != ativo.identificacao:
            if await self.repo.identificacao_exists(kwargs["identificacao"], exclude_id=ativo_id):
                raise ValueError("Já existe um ativo com essa identificação")
        for key, value in kwargs.items():
            if value is not None and hasattr(ativo, key):
                setattr(ativo, key, value)
        return await self.repo.update(ativo)

    async def delete(self, ativo_id: uuid.UUID) -> None:
        ativo = await self.get_by_id(ativo_id)
        await self.repo.delete(ativo)

    async def search(self, query: str) -> list[AtivoModel]:
        return await self.repo.search(query)
