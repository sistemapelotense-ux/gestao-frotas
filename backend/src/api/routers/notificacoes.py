from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.notificacao_service import NotificacaoService
from src.api.schemas.notificacao import NotificacaoResponse, NotificacaoCountResponse
from src.api.dependencies import get_current_user
from src.infrastructure.database.models import UserModel
import uuid

router = APIRouter(prefix="/notificacoes", tags=["Notificações"])


@router.get("", response_model=list[NotificacaoResponse])
async def list_notificacoes(
    lida: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    service = NotificacaoService(db)
    return await service.get_by_usuario(current_user.id, lida, skip, limit)


@router.get("/count", response_model=NotificacaoCountResponse)
async def count_nao_lidas(db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = NotificacaoService(db)
    count = await service.count_nao_lidas(current_user.id)
    return NotificacaoCountResponse(nao_lidas=count)


@router.put("/{notif_id}/ler")
async def marcar_como_lida(notif_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = NotificacaoService(db)
    try:
        await service.marcar_como_lida(notif_id, current_user.id)
        return {"message": "Notificação marcada como lida"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/ler-todas")
async def marcar_todas_como_lidas(db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = NotificacaoService(db)
    await service.marcar_todas_como_lidas(current_user.id)
    return {"message": "Todas as notificações marcadas como lidas"}
