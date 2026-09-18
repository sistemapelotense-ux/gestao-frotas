from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.lancamento_service import LancamentoService
from src.api.schemas.lancamento import LancamentoCreate, LancamentoUpdate, LancamentoResponse
from src.api.dependencies import get_current_user
from src.infrastructure.database.models import UserModel
import uuid

router = APIRouter(prefix="/lancamentos", tags=["Lançamentos Diários"])


@router.get("", response_model=list[LancamentoResponse])
async def list_lancamentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    service = LancamentoService(db)
    return await service.get_by_usuario(current_user, skip, limit)


@router.get("/{lancamento_id}", response_model=LancamentoResponse)
async def get_lancamento(lancamento_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = LancamentoService(db)
    try:
        return await service.get_by_id(lancamento_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=LancamentoResponse, status_code=status.HTTP_201_CREATED)
async def create_lancamento(body: LancamentoCreate, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = LancamentoService(db)
    try:
        return await service.create(body.model_dump(), current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{lancamento_id}", response_model=LancamentoResponse)
async def update_lancamento(lancamento_id: uuid.UUID, body: LancamentoUpdate, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = LancamentoService(db)
    try:
        return await service.update(lancamento_id, body.model_dump(exclude_unset=True), current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lancamento(lancamento_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    service = LancamentoService(db)
    try:
        await service.delete(lancamento_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
