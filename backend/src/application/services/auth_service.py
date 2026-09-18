from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.notificacao_repository import NotificacaoRepository
from src.infrastructure.security.password import hash_password, verify_password
from src.infrastructure.security.jwt import create_access_token
from src.infrastructure.database.models import UserModel, NotificacaoModel
import uuid


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.notificacao_repo = NotificacaoRepository(db)

    async def register(self, email: str, password: str, nome: str, papel: str = "obra", obra_id: uuid.UUID | None = None) -> UserModel:
        if await self.user_repo.email_exists(email):
            raise ValueError("E-mail já cadastrado")
        user = UserModel(
            email=email,
            password_hash=hash_password(password),
            nome=nome,
            papel=papel,
            obra_id=obra_id,
            ativo=True,
        )
        return await self.user_repo.create(user)

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repo.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise ValueError("E-mail ou senha inválidos")
        if not user.ativo:
            raise ValueError("Conta desativada")
        token = create_access_token(data={"sub": str(user.id), "papel": user.papel})
        return {"access_token": token, "token_type": "bearer"}

    async def change_password(self, user: UserModel, current_password: str, new_password: str) -> None:
        if not verify_password(current_password, user.password_hash):
            raise ValueError("Senha atual incorreta")
        user.password_hash = hash_password(new_password)
        await self.user_repo.update(user)

    async def create_notification(self, usuario_id: uuid.UUID, titulo: str, mensagem: str, tipo: str = "info") -> None:
        notif = NotificacaoModel(
            usuario_id=usuario_id,
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo,
            lida=False,
        )
        await self.notificacao_repo.create(notif)
