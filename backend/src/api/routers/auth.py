from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db
from src.application.services.auth_service import AuthService
from src.api.schemas.auth import AuthRegisterRequest, AuthLoginRequest, AuthTokenResponse, AuthChangePasswordRequest
from src.api.dependencies import get_current_user
from src.infrastructure.database.models import UserModel
from src.api.rate_limit import limiter
from src.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def register(request: Request, body: AuthRegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    try:
        user = await service.register(
            email=body.email,
            password=body.password,
            nome=body.nome,
            papel=body.papel,
            obra_id=body.obra_id,
        )
        return {"id": str(user.id), "email": user.email, "nome": user.nome, "papel": user.papel}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/token", response_model=AuthTokenResponse)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def login(request: Request, body: AuthLoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    try:
        result = await service.login(email=body.email, password=body.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me")
async def me(current_user: UserModel = Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "nome": current_user.nome,
        "papel": current_user.papel,
        "obra_id": str(current_user.obra_id) if current_user.obra_id else None,
    }


@router.put("/password")
async def change_password(
    body: AuthChangePasswordRequest,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.new_password != body.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não conferem")
    service = AuthService(db)
    try:
        await service.change_password(current_user, body.current_password, body.new_password)
        return {"message": "Senha alterada com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))