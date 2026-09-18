import uuid
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import ArquivoPropriedadeModel
from src.infrastructure.repositories.base_repository import BaseRepository


class ArquivoPropriedadeRepository(BaseRepository[ArquivoPropriedadeModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ArquivoPropriedadeModel, db)

    async def get_by_ativo(self, ativo_id: uuid.UUID) -> ArquivoPropriedadeModel | None:
        result = await self.db.execute(
            select(ArquivoPropriedadeModel).where(ArquivoPropriedadeModel.ativo_id == ativo_id)
        )
        return result.scalar_one_or_none()

    async def get_by_status(self, status: str) -> list[ArquivoPropriedadeModel]:
        result = await self.db.execute(
            select(ArquivoPropriedadeModel).where(ArquivoPropriedadeModel.status == status)
        )
        return list(result.scalars().all())

    async def get_all_ativos_ids(self) -> list[uuid.UUID]:
        result = await self.db.execute(select(ArquivoPropriedadeModel.ativo_id))
        return [row[0] for row in result.all()]

    async def ativo_exists_in_propriedade(self, ativo_id: uuid.UUID) -> bool:
        result = await self.db.execute(
            select(ArquivoPropriedadeModel.id).where(ArquivoPropriedadeModel.ativo_id == ativo_id)
        )
        return result.scalar_one_or_none() is not None
