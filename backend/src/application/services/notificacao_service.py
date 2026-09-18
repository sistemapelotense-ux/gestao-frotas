from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.repositories.notificacao_repository import NotificacaoRepository
from src.infrastructure.database.models import NotificacaoModel
import uuid


class NotificacaoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = NotificacaoRepository(db)

    async def create(self, usuario_id: uuid.UUID, titulo: str, mensagem: str, tipo: str = "info") -> NotificacaoModel:
        notif = NotificacaoModel(
            usuario_id=usuario_id,
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo,
            lida=False,
        )
        return await self.repo.create(notif)

    async def get_by_usuario(self, usuario_id: uuid.UUID, lida: bool | None = None, skip: int = 0, limit: int = 50) -> list[NotificacaoModel]:
        return await self.repo.get_by_usuario(usuario_id, lida, skip, limit)

    async def count_nao_lidas(self, usuario_id: uuid.UUID) -> int:
        return await self.repo.count_nao_lidas(usuario_id)

    async def marcar_como_lida(self, notif_id: uuid.UUID, usuario_id: uuid.UUID) -> None:
        notif = await self.repo.get_by_id(notif_id)
        if notif is None or notif.usuario_id != usuario_id:
            raise ValueError("Notificação não encontrada")
        notif.lida = True
        await self.repo.update(notif)

    async def marcar_todas_como_lidas(self, usuario_id: uuid.UUID) -> None:
        await self.repo.marcar_todas_como_lidas(usuario_id)
