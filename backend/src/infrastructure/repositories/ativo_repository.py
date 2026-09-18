import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import AtivoModel
from src.infrastructure.repositories.base_repository import BaseRepository


class AtivoRepository(BaseRepository[AtivoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(AtivoModel, db)

    async def get_by_identificacao(self, identificacao: str) -> AtivoModel | None:
        result = await self.db.execute(
            select(AtivoModel).where(AtivoModel.identificacao == identificacao)
        )
        return result.scalar_one_or_none()

    async def search(self, query: str) -> list[AtivoModel]:
        term = f"%{query}%"
        result = await self.db.execute(
            select(AtivoModel).where(
                AtivoModel.identificacao.ilike(term)
                | AtivoModel.descricao.ilike(term)
                | AtivoModel.tipo.ilike(term)
                | AtivoModel.fabricante.ilike(term)
                | AtivoModel.modelo.ilike(term)
            )
        )
        return list(result.scalars().all())

    async def identificacao_exists(self, identificacao: str, exclude_id: uuid.UUID | None = None) -> bool:
        q = select(AtivoModel.id).where(AtivoModel.identificacao == identificacao)
        if exclude_id:
            q = q.where(AtivoModel.id != exclude_id)
        result = await self.db.execute(q)
        return result.scalar_one_or_none() is not None
