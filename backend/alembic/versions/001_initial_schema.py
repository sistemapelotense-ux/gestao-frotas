"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-09-16
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "obra",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("localizacao", sa.String(500), nullable=False),
        sa.Column("ativa", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "usuario",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("nome", sa.String(255), nullable=False),
        sa.Column("papel", sa.String(20), nullable=False, server_default="obra"),
        sa.Column("obra_id", UUID(as_uuid=True), sa.ForeignKey("obra.id"), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_usuario_email", "usuario", ["email"])

    op.create_table(
        "ativo",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("identificacao", sa.String(100), nullable=False, unique=True),
        sa.Column("descricao", sa.String(500), nullable=False, server_default=""),
        sa.Column("tipo", sa.String(100), nullable=False, server_default=""),
        sa.Column("fabricante", sa.String(255), nullable=False, server_default=""),
        sa.Column("modelo", sa.String(255), nullable=False, server_default=""),
        sa.Column("status", sa.String(20), nullable=False, server_default="disponivel"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_ativo_identificacao", "ativo", ["identificacao"])

    op.create_table(
        "lancamento_diario",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("data", sa.DateTime(), nullable=False),
        sa.Column("ativo_id", UUID(as_uuid=True), sa.ForeignKey("ativo.id"), nullable=False),
        sa.Column("obra_id", UUID(as_uuid=True), sa.ForeignKey("obra.id"), nullable=False),
        sa.Column("usuario_id", UUID(as_uuid=True), sa.ForeignKey("usuario.id"), nullable=False),
        sa.Column("status_uso", sa.String(5), nullable=False),
        sa.Column("informacoes_dia", sa.String(500), nullable=False, server_default=""),
        sa.Column("codigo_ativo", sa.String(100), nullable=False, server_default=""),
        sa.Column("descricao", sa.String(500), nullable=False, server_default=""),
        sa.Column("tipo", sa.String(100), nullable=False, server_default=""),
        sa.Column("fabricante", sa.String(255), nullable=False, server_default=""),
        sa.Column("modelo", sa.String(255), nullable=False, server_default=""),
        sa.Column("horimetro_inicial", sa.Float(), nullable=False, server_default="0"),
        sa.Column("horimetro_final", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_horas", sa.Float(), nullable=False, server_default="0"),
        sa.Column("km_inicial", sa.Float(), nullable=False, server_default="0"),
        sa.Column("km_final", sa.Float(), nullable=False, server_default="0"),
        sa.Column("total_km", sa.Float(), nullable=False, server_default="0"),
        sa.Column("descritivo_manutencao", sa.Text(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pendente"),
        sa.Column("condicao_climatica", sa.String(50), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "arquivo_de_propriedade",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("ativo_id", UUID(as_uuid=True), sa.ForeignKey("ativo.id"), nullable=False),
        sa.Column("status", sa.String(10), nullable=False, server_default="P"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "notificacao",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("usuario_id", UUID(as_uuid=True), sa.ForeignKey("usuario.id"), nullable=False),
        sa.Column("titulo", sa.String(255), nullable=False),
        sa.Column("mensagem", sa.Text(), nullable=False),
        sa.Column("lida", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("tipo", sa.String(50), nullable=False, server_default="info"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "upload",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("usuario_id", UUID(as_uuid=True), sa.ForeignKey("usuario.id"), nullable=False),
        sa.Column("nome_arquivo", sa.String(255), nullable=False),
        sa.Column("caminho", sa.String(500), nullable=False),
        sa.Column("tamanho", sa.Integer(), nullable=False),
        sa.Column("tipo_mime", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("upload")
    op.drop_table("notificacao")
    op.drop_table("arquivo_de_propriedade")
    op.drop_table("lancamento_diario")
    op.drop_index("ix_ativo_identificacao", table_name="ativo")
    op.drop_table("ativo")
    op.drop_index("ix_usuario_email", table_name="usuario")
    op.drop_table("usuario")
    op.drop_table("obra")
