from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.consolidacao_service import ConsolidacaoService
from src.api.dependencies import require_admin
from src.infrastructure.database.models import UserModel

router = APIRouter(prefix="/consolidacao", tags=["Consolidação"])


@router.post("/executar")
async def executar_consolidacao(db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ConsolidacaoService(db)
    result = await service.consolidar()
    return result
