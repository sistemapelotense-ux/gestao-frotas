import uuid
from datetime import datetime
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.infrastructure.database.models import LancamentoDiarioModel
from src.infrastructure.repositories.base_repository import BaseRepository


class LancamentoRepository(BaseRepository[LancamentoDiarioModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(LancamentoDiarioModel, db)

    async def get_by_obra_and_date(self, obra_id: uuid.UUID, data: datetime) -> list[LancamentoDiarioModel]:
        day_start = data.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = data.replace(hour=23, minute=59, second=59, microsecond=999999)
        result = await self.db.execute(
            select(LancamentoDiarioModel).where(
                and_(
                    LancamentoDiarioModel.obra_id == obra_id,
                    LancamentoDiarioModel.data >= day_start,
                    LancamentoDiarioModel.data <= day_end,
                )
            )
        )
        return list(result.scalars().all())

    async def get_by_ativo_and_date(self, ativo_id: uuid.UUID, data: datetime) -> list[LancamentoDiarioModel]:
        day_start = data.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = data.replace(hour=23, minute=59, second=59, microsecond=999999)
        result = await self.db.execute(
            select(LancamentoDiarioModel).where(
                and_(
                    LancamentoDiarioModel.ativo_id == ativo_id,
                    LancamentoDiarioModel.data >= day_start,
                    LancamentoDiarioModel.data <= day_end,
                )
            )
        )
        return list(result.scalars().all())

    async def get_by_date_range(self, start: datetime, end: datetime) -> list[LancamentoDiarioModel]:
        result = await self.db.execute(
            select(LancamentoDiarioModel).where(
                and_(
                    LancamentoDiarioModel.data >= start,
                    LancamentoDiarioModel.data <= end,
                )
            )
        )
        return list(result.scalars().all())

    async def get_by_usuario(self, usuario_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[LancamentoDiarioModel]:
        result = await self.db.execute(
            select(LancamentoDiarioModel)
            .where(LancamentoDiarioModel.usuario_id == usuario_id)
            .order_by(LancamentoDiarioModel.data.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_obra(self, obra_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[LancamentoDiarioModel]:
        result = await self.db.execute(
            select(LancamentoDiarioModel)
            .where(LancamentoDiarioModel.obra_id == obra_id)
            .order_by(LancamentoDiarioModel.data.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def check_duplicate(self, ativo_id: uuid.UUID, data: datetime, exclude_id: uuid.UUID | None = None) -> list[LancamentoDiarioModel]:
        day_start = data.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = data.replace(hour=23, minute=59, second=59, microsecond=999999)
        q = select(LancamentoDiarioModel).where(
            and_(
                LancamentoDiarioModel.ativo_id == ativo_id,
                LancamentoDiarioModel.data >= day_start,
                LancamentoDiarioModel.data <= day_end,
            )
        )
        if exclude_id:
            q = q.where(LancamentoDiarioModel.id != exclude_id)
        result = await self.db.execute(q)
        return list(result.scalars().all())
