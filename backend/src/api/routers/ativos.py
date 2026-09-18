from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.ativo_service import AtivoService
from src.api.schemas.ativo import AtivoCreate, AtivoUpdate, AtivoResponse
from src.api.dependencies import get_current_user, require_admin
from src.infrastructure.database.models import UserModel
import uuid

router = APIRouter(prefix="/ativos", tags=["Ativos"])


@router.get("", response_model=list[AtivoResponse])
async def list_ativos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
    _user: UserModel = Depends(get_current_user),
):
    service = AtivoService(db)
    if search:
        return await service.search(search)
    return await service.get_all(skip, limit)


@router.get("/{ativo_id}", response_model=AtivoResponse)
async def get_ativo(ativo_id: uuid.UUID, db: AsyncSession = Depends(get_db), _user: UserModel = Depends(get_current_user)):
    service = AtivoService(db)
    try:
        return await service.get_by_id(ativo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=AtivoResponse, status_code=status.HTTP_201_CREATED)
async def create_ativo(body: AtivoCreate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = AtivoService(db)
    try:
        return await service.create(
            identificacao=body.identificacao,
            descricao=body.descricao,
            tipo=body.tipo,
            fabricante=body.fabricante,
            modelo=body.modelo,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{ativo_id}", response_model=AtivoResponse)
async def update_ativo(ativo_id: uuid.UUID, body: AtivoUpdate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = AtivoService(db)
    try:
        return await service.update(ativo_id, **body.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{ativo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ativo(ativo_id: uuid.UUID, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = AtivoService(db)
    try:
        await service.delete(ativo_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
