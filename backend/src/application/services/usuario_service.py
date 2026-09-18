from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password import hash_password
from src.infrastructure.database.models import UserModel
import uuid


class UsuarioService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)

    async def create(self, email: str, password: str, nome: str, papel: str = "obra", obra_id: uuid.UUID | None = None) -> UserModel:
        if await self.repo.email_exists(email):
            raise ValueError("E-mail já cadastrado")
        user = UserModel(
            email=email,
            password_hash=hash_password(password),
            nome=nome,
            papel=papel,
            obra_id=obra_id,
            ativo=True,
        )
        return await self.repo.create(user)

    async def get_by_id(self, user_id: uuid.UUID) -> UserModel:
        user = await self.repo.get_by_id(user_id)
        if user is None:
            raise ValueError("Usuário não encontrado")
        return user

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[UserModel]:
        return await self.repo.get_all(skip, limit)

    async def update(self, user_id: uuid.UUID, **kwargs) -> UserModel:
        user = await self.get_by_id(user_id)
        if "password" in kwargs and kwargs["password"]:
            user.password_hash = hash_password(kwargs.pop("password"))
        if "email" in kwargs and kwargs["email"] != user.email:
            if await self.repo.email_exists(kwargs["email"]):
                raise ValueError("E-mail já cadastrado")
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        return await self.repo.update(user)

    async def delete(self, user_id: uuid.UUID) -> None:
        user = await self.get_by_id(user_id)
        user.ativo = False
        await self.repo.update(user)
