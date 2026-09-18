from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.arquivo_propriedade_service import ArquivoPropriedadeService
from src.api.schemas.arquivo_propriedade import ArquivoPropriedadeCreate, ArquivoPropriedadeUpdate, ArquivoPropriedadeResponse
from src.api.dependencies import get_current_user, require_admin
from src.infrastructure.database.models import UserModel
import uuid

router = APIRouter(prefix="/arquivo-propriedade", tags=["Arquivo de Propriedade"])


@router.get("", response_model=list[ArquivoPropriedadeResponse])
async def list_arquivo(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    status_filter: str | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    _user: UserModel = Depends(get_current_user),
):
    service = ArquivoPropriedadeService(db)
    if status_filter:
        return await service.get_by_status(status_filter)
    return await service.get_all(skip, limit)


@router.get("/{prop_id}", response_model=ArquivoPropriedadeResponse)
async def get_arquivo(prop_id: uuid.UUID, db: AsyncSession = Depends(get_db), _user: UserModel = Depends(get_current_user)):
    service = ArquivoPropriedadeService(db)
    try:
        return await service.get_by_id(prop_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=ArquivoPropriedadeResponse, status_code=status.HTTP_201_CREATED)
async def create_arquivo(body: ArquivoPropriedadeCreate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ArquivoPropriedadeService(db)
    try:
        return await service.create(ativo_id=body.ativo_id, status=body.status)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{prop_id}", response_model=ArquivoPropriedadeResponse)
async def update_arquivo(prop_id: uuid.UUID, body: ArquivoPropriedadeUpdate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ArquivoPropriedadeService(db)
    try:
        return await service.update(prop_id, status=body.status)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{prop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_arquivo(prop_id: uuid.UUID, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ArquivoPropriedadeService(db)
    try:
        await service.delete(prop_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
