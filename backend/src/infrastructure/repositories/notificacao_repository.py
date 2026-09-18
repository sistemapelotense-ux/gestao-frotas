import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import NotificacaoModel
from src.infrastructure.repositories.base_repository import BaseRepository


class NotificacaoRepository(BaseRepository[NotificacaoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(NotificacaoModel, db)

    async def get_by_usuario(self, usuario_id: uuid.UUID, lida: bool | None = None, skip: int = 0, limit: int = 50) -> list[NotificacaoModel]:
        q = select(NotificacaoModel).where(NotificacaoModel.usuario_id == usuario_id)
        if lida is not None:
            q = q.where(NotificacaoModel.lida == lida)
        q = q.order_by(NotificacaoModel.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(q)
        return list(result.scalars().all())

    async def count_nao_lidas(self, usuario_id: uuid.UUID) -> int:
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count(NotificacaoModel.id)).where(
                NotificacaoModel.usuario_id == usuario_id,
                NotificacaoModel.lida == False,
            )
        )
        return result.scalar_one()

    async def marcar_todas_como_lidas(self, usuario_id: uuid.UUID) -> None:
        await self.db.execute(
            update(NotificacaoModel)
            .where(NotificacaoModel.usuario_id == usuario_id, NotificacaoModel.lida == False)
            .values(lida=True)
        )
        await self.db.commit()
