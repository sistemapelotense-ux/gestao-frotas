import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models import UserModel
from src.infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def get_by_obra(self, obra_id: uuid.UUID) -> list[UserModel]:
        result = await self.db.execute(
            select(UserModel).where(UserModel.obra_id == obra_id, UserModel.ativo == True)
        )
        return list(result.scalars().all())

    async def email_exists(self, email: str) -> bool:
        result = await self.db.execute(select(UserModel.id).where(UserModel.email == email))
        return result.scalar_one_or_none() is not None
