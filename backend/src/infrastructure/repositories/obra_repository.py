from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import ObraModel
from src.infrastructure.repositories.base_repository import BaseRepository


class ObraRepository(BaseRepository[ObraModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ObraModel, db)

    async def get_by_nome(self, nome: str) -> ObraModel | None:
        result = await self.db.execute(select(ObraModel).where(ObraModel.nome == nome))
        return result.scalar_one_or_none()

    async def search(self, query: str) -> list[ObraModel]:
        term = f"%{query}%"
        result = await self.db.execute(
            select(ObraModel).where(
                ObraModel.nome.ilike(term) | ObraModel.localizacao.ilike(term)
            )
        )
        return list(result.scalars().all())
