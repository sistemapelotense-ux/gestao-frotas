import uuid
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.session import Base


class UserModel(Base):
    __tablename__ = "usuario"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    papel: Mapped[str] = mapped_column(String(20), nullable=False, default="obra")
    obra_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("obra.id"), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    obra = relationship("ObraModel", back_populates="usuarios")
    lancamentos = relationship("LancamentoDiarioModel", back_populates="usuario")
    notificacoes = relationship("NotificacaoModel", back_populates="usuario")


class ObraModel(Base):
    __tablename__ = "obra"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    localizacao: Mapped[str] = mapped_column(String(500), nullable=False)
    ativa: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    usuarios = relationship("UserModel", back_populates="obra")
    lancamentos = relationship("LancamentoDiarioModel", back_populates="obra")


class AtivoModel(Base):
    __tablename__ = "ativo"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identificacao: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    tipo: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    fabricante: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    modelo: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="disponivel")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    lancamentos = relationship("LancamentoDiarioModel", back_populates="ativo")
    arquivo_propriedade = relationship("ArquivoPropriedadeModel", back_populates="ativo")


class LancamentoDiarioModel(Base):
    __tablename__ = "lancamento_diario"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    ativo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ativo.id"), nullable=False)
    obra_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("obra.id"), nullable=False)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    status_uso: Mapped[str] = mapped_column(String(5), nullable=False)
    informacoes_dia: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    codigo_ativo: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    descricao: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    tipo: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    fabricante: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    modelo: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    horimetro_inicial: Mapped[float] = mapped_column(nullable=False, default=0.0)
    horimetro_final: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_horas: Mapped[float] = mapped_column(nullable=False, default=0.0)
    km_inicial: Mapped[float] = mapped_column(nullable=False, default=0.0)
    km_final: Mapped[float] = mapped_column(nullable=False, default=0.0)
    total_km: Mapped[float] = mapped_column(nullable=False, default=0.0)
    descritivo_manutencao: Mapped[str] = mapped_column(Text, nullable=True, default="")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pendente")
    condicao_climatica: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    ativo = relationship("AtivoModel", back_populates="lancamentos")
    obra = relationship("ObraModel", back_populates="lancamentos")
    usuario = relationship("UserModel", back_populates="lancamentos")


class ArquivoPropriedadeModel(Base):
    __tablename__ = "arquivo_de_propriedade"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ativo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("ativo.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="P")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    ativo = relationship("AtivoModel", back_populates="arquivo_propriedade")


class NotificacaoModel(Base):
    __tablename__ = "notificacao"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    mensagem: Mapped[str] = mapped_column(Text, nullable=False)
    lida: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, default="info")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    usuario = relationship("UserModel", back_populates="notificacoes")


class UploadModel(Base):
    __tablename__ = "upload"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuario.id"), nullable=False)
    nome_arquivo: Mapped[str] = mapped_column(String(255), nullable=False)
    caminho: Mapped[str] = mapped_column(String(500), nullable=False)
    tamanho: Mapped[int] = mapped_column(nullable=False)
    tipo_mime: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
