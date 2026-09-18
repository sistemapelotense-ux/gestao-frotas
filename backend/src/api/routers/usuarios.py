from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.usuario_service import UsuarioService
from src.api.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from src.api.dependencies import require_admin
from src.infrastructure.database.models import UserModel
import uuid

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("", response_model=list[UsuarioResponse])
async def list_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
    _admin: UserModel = Depends(require_admin),
):
    service = UsuarioService(db)
    return await service.get_all(skip, limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: uuid.UUID, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = UsuarioService(db)
    try:
        return await service.get_by_id(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(body: UsuarioCreate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = UsuarioService(db)
    try:
        return await service.create(
            email=body.email,
            password=body.password,
            nome=body.nome,
            papel=body.papel,
            obra_id=body.obra_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(usuario_id: uuid.UUID, body: UsuarioUpdate, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = UsuarioService(db)
    try:
        return await service.update(usuario_id, **body.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: uuid.UUID, db: AsyncSession = Depends(get_db), _admin: UserModel = Depends(require_admin)):
    service = UsuarioService(db)
    try:
        await service.delete(usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
