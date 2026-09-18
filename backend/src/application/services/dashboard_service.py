from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from src.infrastructure.database.models import LancamentoDiarioModel, AtivoModel, ObraModel, ArquivoPropriedadeModel
from src.infrastructure.repositories.lancamento_repository import LancamentoRepository
from src.infrastructure.repositories.ativo_repository import AtivoRepository
from src.infrastructure.repositories.obra_repository import ObraRepository
from src.infrastructure.repositories.arquivo_propriedade_repository import ArquivoPropriedadeRepository

LOCACAO_STATUSES = {"O", "D", "P", "C", "R"}


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.lancamento_repo = LancamentoRepository(db)
        self.ativo_repo = AtivoRepository(db)
        self.obra_repo = ObraRepository(db)
        self.arquivo_repo = ArquivoPropriedadeRepository(db)

    async def get_resumo(self) -> dict:
        hoje = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

        total_ativos = await self.ativo_repo.count()
        total_obras = await self.obra_repo.count()

        day_start = hoje
        day_end = hoje.replace(hour=23, minute=59, second=59, microsecond=999999)

        from sqlalchemy import select, func
        result = await self.db.execute(
            select(func.count(LancamentoDiarioModel.id)).where(
                and_(
                    LancamentoDiarioModel.data >= day_start,
                    LancamentoDiarioModel.data <= day_end,
                )
            )
        )
        total_lancamentos_hoje = result.scalar_one()

        ativos_propriedade = await self.arquivo_repo.get_all()
        ativos_alocados_hoje = set()
        result_lanc = await self.db.execute(
            select(LancamentoDiarioModel.ativo_id).where(
                and_(
                    LancamentoDiarioModel.data >= day_start,
                    LancamentoDiarioModel.data <= day_end,
                    LancamentoDiarioModel.status_uso.in_(list(LOCACAO_STATUSES)),
                )
            )
        )
        for row in result_lanc.all():
            ativos_alocados_hoje.add(row[0])

        ativos_nao_alocados = [
            ap for ap in ativos_propriedade
            if ap.ativo_id not in ativos_alocados_hoje
        ]

        ativos_ids = [ap.ativo_id for ap in ativos_propriedade]
        ativo_identificacao: dict[uuid.UUID, str] = {}
        if ativos_ids:
            result_ativo = await self.db.execute(
                select(AtivoModel.id, AtivoModel.identificacao).where(AtivoModel.id.in_(ativos_ids))
            )
            for ativo_row in result_ativo.all():
                ativo_identificacao[ativo_row[0]] = ativo_row[1]

        ativo_obras_map: dict[str, set[str]] = {}
        result_todos = await self.db.execute(
            select(LancamentoDiarioModel).where(
                and_(
                    LancamentoDiarioModel.data >= day_start,
                    LancamentoDiarioModel.data <= day_end,
                )
            )
        )
        for lanc in result_todos.scalars().all():
            key = str(lanc.ativo_id)
            ativo_obras_map.setdefault(key, set()).add(str(lanc.obra_id))

        duplicidades = []
        for aid, obs in ativo_obras_map.items():
            if len(obs) > 1:
                duplicidades.append({"ativo_id": aid, "obras": list(obs)})

        return {
            "total_ativos": total_ativos,
            "total_obras": total_obras,
            "lancamentos_hoje": total_lancamentos_hoje,
            "ativos_alocados_hoje": len(ativos_alocados_hoje),
            "ativos_nao_alocados": len(ativos_nao_alocados),
            "duplicidades_hoje": len(duplicidades),
            "detalhe_nao_alocados": [
                {"ativo_id": str(ap.ativo_id), "identificacao": ativo_identificacao.get(ap.ativo_id, "")}
                for ap in ativos_nao_alocados[:20]
            ],
            "detalhe_duplicidades": duplicidades[:20],
        }

    async def get_ultimos_lancamentos(self, limit: int = 10) -> list[dict]:
        result = await self.db.execute(
            select(LancamentoDiarioModel)
            .order_by(LancamentoDiarioModel.created_at.desc())
            .limit(limit)
        )
        lancamentos = result.scalars().all()
        out = []
        for l in lancamentos:
            ativo = await self.ativo_repo.get_by_id(l.ativo_id)
            obra = await self.obra_repo.get_by_id(l.obra_id)
            out.append({
                "id": str(l.id),
                "data": l.data.strftime("%d/%m/%Y"),
                "ativo": ativo.identificacao if ativo else "",
                "obra": obra.nome if obra else "",
                "status_uso": l.status_uso,
            })
        return out
