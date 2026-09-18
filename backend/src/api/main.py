import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from src.config import get_settings
from src.infrastructure.database.session import engine, Base, async_session
from src.infrastructure.database.models import (
    UserModel, ObraModel, AtivoModel,
    LancamentoDiarioModel, ArquivoPropriedadeModel,
    NotificacaoModel, UploadModel,
)
from src.infrastructure.security.password import hash_password
from src.infrastructure.jobs.scheduler import start_scheduler
from src.api.rate_limit import limiter
from src.api.routers import (
    auth, ativos, obras, usuarios, lancamentos,
    arquivo_propriedade, notificacoes, dashboard,
    consolidacao, upload,
)
from sqlalchemy import select

settings = get_settings()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_admin():
    from src.infrastructure.repositories.user_repository import UserRepository
    async with async_session() as db:
        repo = UserRepository(db)
        admin = await repo.get_by_email(settings.ADMIN_EMAIL)
        if admin is None:
            admin = UserModel(
                email=settings.ADMIN_EMAIL,
                password_hash=hash_password(settings.ADMIN_PASSWORD),
                nome=settings.ADMIN_NAME,
                papel="admin",
                ativo=True,
            )
            await repo.create(admin)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await seed_admin()
    os.makedirs(settings.STORAGE_PATH, exist_ok=True)
    start_scheduler()
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(ativos.router, prefix=settings.API_PREFIX)
app.include_router(obras.router, prefix=settings.API_PREFIX)
app.include_router(usuarios.router, prefix=settings.API_PREFIX)
app.include_router(lancamentos.router, prefix=settings.API_PREFIX)
app.include_router(arquivo_propriedade.router, prefix=settings.API_PREFIX)
app.include_router(notificacoes.router, prefix=settings.API_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_PREFIX)
app.include_router(consolidacao.router, prefix=settings.API_PREFIX)
app.include_router(upload.router, prefix=settings.API_PREFIX)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"},
    )
