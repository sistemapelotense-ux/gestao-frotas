from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.dashboard_service import DashboardService
from src.api.schemas.dashboard import DashboardResumo, DashboardLancamento
from src.api.dependencies import get_current_user
from src.infrastructure.database.models import UserModel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResumo)
async def get_dashboard(db: AsyncSession = Depends(get_db), _user: UserModel = Depends(get_current_user)):
    service = DashboardService(db)
    return await service.get_resumo()


@router.get("/lancamentos-recentes", response_model=list[DashboardLancamento])
async def get_ultimos_lancamentos(db: AsyncSession = Depends(get_db), _user: UserModel = Depends(get_current_user)):
    service = DashboardService(db)
    return await service.get_ultimos_lancamentos(10)
