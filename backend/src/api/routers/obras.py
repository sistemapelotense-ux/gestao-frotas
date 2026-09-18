from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.obra_service import ObraService
from src.api.schemas.obra import ObraCreate, ObraUpdate, ObraResponse
from src.api.dependencies import get_current_user, require_admin
from src.infrastructure.database.models import UserModel
import uuid

router = APIRouter(prefix="/obras", tags=["Obras"])


@router.get("", response_model=list[ObraResponse])
async def list_obras(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: str | None = None,
    db: AsyncSession = Depends(get_db),
    _user: UserModel = Depends(get_current_user),
):
    service = ObraService(db)
    if search:
        return await service.search(search)
    return await service.get_all(skip, limit)


@router.get("/{obra_id}", response_model=ObraResponse)
async def get_obra(obra_id: uuid.UUID, db: AsyncSession = Depends(get_db), _user: UserModel = Depends(get_current_user)):
    service = ObraService(db)
    try:
        return await service.get_by_id(obra_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=ObraResponse, status_code=status.HTTP_201_CREATED)
async def create_obra(body: ObraCreate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ObraService(db)
    return await service.create(nome=body.nome, localizacao=body.localizacao)


@router.put("/{obra_id}", response_model=ObraResponse)
async def update_obra(obra_id: uuid.UUID, body: ObraUpdate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ObraService(db)
    try:
        return await service.update(obra_id, **body.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{obra_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_obra(obra_id: uuid.UUID, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = ObraService(db)
    try:
        await service.delete(obra_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
