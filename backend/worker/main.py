"""Worker de emissão de certificados (ADR-04).

Consome `job_certificado` usando `FOR UPDATE SKIP LOCKED`, o que permite rodar
várias instâncias em paralelo sem processar o mesmo job duas vezes.

Executar:  python -m worker.main   (ou `docker compose up worker`)
Backlog: GE-105 (fila), GE-106 (PDF/A), GE-107 (Storage).
"""

import asyncio
import logging

from sqlalchemy import text

from app.core.database import SessionLocal

logger = logging.getLogger("worker")

INTERVALO_SEGUNDOS = 3
MAX_TENTATIVAS = 3

_SQL_PEGAR_JOB = text(
    """
    update public.job_certificado j
       set status = 'processando', iniciado_em = now(), tentativas = j.tentativas + 1
     where j.id = (
         select id from public.job_certificado
          where status = 'pendente'
          order by criado_em
          for update skip locked
          limit 1
     )
    returning j.id, j.evento_id, j.tipo, j.payload, j.tentativas
    """
)


async def processar_job(job) -> None:
    """TODO (GE-106): para cada elegível do payload, gerar o PDF/A com
    `worker.pdf.gerar_certificado_pdf`, enviar ao Storage, gravar `certificado`
    e registrar `certificado_emitido` na auditoria (responsável = Sistema)."""
    logger.info("Processando job %s (%s) do evento %s", job.id, job.tipo, job.evento_id)
    raise NotImplementedError("Geração de certificados ainda não implementada (GE-106)")


async def executar_uma_vez() -> bool:
    """Processa no máximo um job. Retorna True se havia job na fila."""
    async with SessionLocal() as session:
        job = (await session.execute(_SQL_PEGAR_JOB)).first()
        await session.commit()
    if job is None:
        return False

    try:
        await processar_job(job)
        novo_status, erro = "concluido", None
    except Exception as exc:  # noqa: BLE001 — qualquer falha vira erro do job
        logger.exception("Falha no job %s", job.id)
        novo_status = "erro" if job.tentativas >= MAX_TENTATIVAS else "pendente"
        erro = str(exc)

    async with SessionLocal() as session:
        await session.execute(
            text(
                "update public.job_certificado set status = :s, erro = :e, "
                "finalizado_em = case when :s in ('concluido', 'erro') then now() end "
                "where id = :id"
            ),
            {"s": novo_status, "e": erro, "id": job.id},
        )
        await session.commit()
    return True


async def loop() -> None:
    logger.info("Worker de certificados iniciado")
    while True:
        tinha_job = await executar_uma_vez()
        if not tinha_job:
            await asyncio.sleep(INTERVALO_SEGUNDOS)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(loop())
