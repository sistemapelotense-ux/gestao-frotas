from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.obra_repository import ObraRepository
from src.infrastructure.database.models import ObraModel
import uuid


class ObraService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ObraRepository(db)

    async def create(self, nome: str, localizacao: str) -> ObraModel:
        obra = ObraModel(nome=nome, localizacao=localizacao, ativa=True)
        return await self.repo.create(obra)

    async def get_by_id(self, obra_id: uuid.UUID) -> ObraModel:
        obra = await self.repo.get_by_id(obra_id)
        if obra is None:
            raise ValueError("Obra não encontrada")
        return obra

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ObraModel]:
        return await self.repo.get_all(skip, limit)

    async def update(self, obra_id: uuid.UUID, **kwargs) -> ObraModel:
        obra = await self.get_by_id(obra_id)
        for key, value in kwargs.items():
            if value is not None and hasattr(obra, key):
                setattr(obra, key, value)
        return await self.repo.update(obra)

    async def delete(self, obra_id: uuid.UUID) -> None:
        obra = await self.get_by_id(obra_id)
        await self.repo.delete(obra)

    async def search(self, query: str) -> list[ObraModel]:
        return await self.repo.search(query)
