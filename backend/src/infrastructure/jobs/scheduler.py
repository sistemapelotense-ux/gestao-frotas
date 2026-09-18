import asyncio
import logging
from datetime import datetime, time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.application.services.consolidacao_service import ConsolidacaoService
from src.infrastructure.database.session import async_session

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def job_consolidacao_diaria():
    logger.info("Executando consolidação diária")
    async with async_session() as db:
        service = ConsolidacaoService(db)
        try:
            result = await service.consolidar()
            logger.info("Consolidação executada: %s dias processados", result.get("dias_processados", 0))
        except Exception as e:
            logger.error("Erro na consolidação diária: %s", e)


def start_scheduler():
    scheduler.add_job(
        job_consolidacao_diaria,
        CronTrigger(hour=23, minute=30),
        id="consolidacao_diaria",
        name="Consolidação diária automática",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler iniciado")