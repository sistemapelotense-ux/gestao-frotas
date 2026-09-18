from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from src.infrastructure.repositories.lancamento_repository import LancamentoRepository
from src.infrastructure.repositories.arquivo_propriedade_repository import ArquivoPropriedadeRepository
from src.infrastructure.repositories.obra_repository import ObraRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.database.models import LancamentoDiarioModel, AtivoModel, ObraModel, NotificacaoModel, UserModel
from src.infrastructure.database.session import async_session

LOCACAO_STATUSES = {"O", "D", "P", "C", "R"}


class ConsolidacaoService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.lancamento_repo = LancamentoRepository(db)
        self.arquivo_repo = ArquivoPropriedadeRepository(db)
        self.obra_repo = ObraRepository(db)
        self.user_repo = UserRepository(db)

    async def consolidar(self, data_inicio: datetime | None = None) -> dict:
        hoje = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if data_inicio is None:
            data_inicio = hoje - timedelta(days=30)
        data_fim = hoje - timedelta(days=1)

        if data_fim < data_inicio:
            return {"erro": "Nenhum dia anterior disponível para consolidação"}

        todas_obras = await self.obra_repo.get_all()
        obras_ids = [str(o.id) for o in todas_obras]

        dias_processados = []
        dias_com_obra_sem_registro = []
        current = data_inicio

        while current <= data_fim:
            lancamentos_dia = await self.lancamento_repo.get_by_date_range(
                current.replace(hour=0, minute=0, second=0, microsecond=0),
                current.replace(hour=23, minute=59, second=59, microsecond=999999),
            )
            obras_com_registro = set(str(l.obra_id) for l in lancamentos_dia)
            obras_sem = [o for o in todas_obras if str(o.id) not in obras_com_registro]

            if obras_sem:
                dias_com_obra_sem_registro.append({
                    "data": current.strftime("%d/%m/%Y"),
                    "obras_sem_registro": [{"id": str(o.id), "nome": o.nome} for o in obras_sem],
                })
            else:
                ativos_ids_lancados = set(str(l.ativo_id) for l in lancamentos_dia)
                todos_ativos_propriedade = await self.arquivo_repo.get_all_ativos_ids()
                ativos_nao_alocados = [
                    str(aid) for aid in todos_ativos_propriedade
                    if str(aid) not in ativos_ids_lancados
                ]

                duplicidades = []
                ativo_obras_map: dict[str, set[str]] = {}
                for l in lancamentos_dia:
                    key = str(l.ativo_id)
                    ativo_obras_map.setdefault(key, set()).add(str(l.obra_id))
                for aid, obs in ativo_obras_map.items():
                    if len(obs) > 1:
                        duplicidades.append({"ativo_id": aid, "obras": list(obs)})

                dias_processados.append({
                    "data": current.strftime("%d/%m/%Y"),
                    "total_lancamentos": len(lancamentos_dia),
                    "ativos_nao_alocados": ativos_nao_alocados,
                    "duplicidades": duplicidades,
                })

                if ativos_nao_alocados or duplicidades:
                    await self._gerar_notificacoes(current, ativos_nao_alocados, duplicidades)

            current += timedelta(days=1)

        return {
            "periodo": {
                "inicio": data_inicio.strftime("%d/%m/%Y"),
                "fim": data_fim.strftime("%d/%m/%Y"),
            },
            "dias_processados": len(dias_processados),
            "dias_com_obra_sem_registro": dias_com_obra_sem_registro,
            "detalhes": dias_processados,
        }

    async def _gerar_notificacoes(self, data: datetime, nao_alocados: list[str], duplicidades: list[dict]) -> None:
        admin_users = await self.user_repo.get_all()
        admins = [u for u in admin_users if u.papel == "admin"]

        notificacoes = []
        for admin in admins:
            if nao_alocados:
                notificacoes.append(
                    NotificacaoModel(
                        usuario_id=admin.id,
                        titulo=f"Ativos não alocados em {data.strftime('%d/%m/%Y')}",
                        mensagem=f"{len(nao_alocados)} ativo(s) não alocado(s) em nenhuma obra nesta data.",
                        tipo="alerta",
                    )
                )
            if duplicidades:
                notificacoes.append(
                    NotificacaoModel(
                        usuario_id=admin.id,
                        titulo=f"Duplicidade detectada em {data.strftime('%d/%m/%Y')}",
                        mensagem=f"{len(duplicidades)} ativo(s) lancado(s) em mais de uma obra.",
                        tipo="alerta",
                    )
                )
        if notificacoes:
            self.db.add_all(notificacoes)
            await self.db.commit()
