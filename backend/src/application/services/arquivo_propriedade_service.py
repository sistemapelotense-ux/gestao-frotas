from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.arquivo_propriedade_repository import ArquivoPropriedadeRepository
from src.infrastructure.database.models import ArquivoPropriedadeModel
import uuid


class ArquivoPropriedadeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ArquivoPropriedadeRepository(db)

    async def create(self, ativo_id: uuid.UUID, status: str = "P") -> ArquivoPropriedadeModel:
        existing = await self.repo.get_by_ativo(ativo_id)
        if existing:
            raise ValueError("Este ativo já está no arquivo de propriedade")
        prop = ArquivoPropriedadeModel(ativo_id=ativo_id, status=status)
        return await self.repo.create(prop)

    async def get_by_id(self, prop_id: uuid.UUID) -> ArquivoPropriedadeModel:
        prop = await self.repo.get_by_id(prop_id)
        if prop is None:
            raise ValueError("Registro não encontrado no arquivo de propriedade")
        return prop

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ArquivoPropriedadeModel]:
        return await self.repo.get_all(skip, limit)

    async def get_by_status(self, status: str) -> list[ArquivoPropriedadeModel]:
        return await self.repo.get_by_status(status)

    async def update(self, prop_id: uuid.UUID, status: str) -> ArquivoPropriedadeModel:
        prop = await self.get_by_id(prop_id)
        prop.status = status
        return await self.repo.update(prop)

    async def delete(self, prop_id: uuid.UUID) -> None:
        prop = await self.get_by_id(prop_id)
        await self.repo.delete(prop)
