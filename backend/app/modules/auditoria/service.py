"""Registro de ações de impacto (RF-011, RN 10.1, RNF-009).

Chame `registrar` com a MESMA sessão usada na ação de impacto: o log só é gravado
se a ação for confirmada, e a ação não é confirmada sem o log.
"""

from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import RegraNegocioViolada
from app.modules.auditoria.models import AcaoAuditoria, LogAuditoria

# Ações administrativas que exigem justificativa (RN 10.1 / RN 10.2)
ACOES_COM_JUSTIFICATIVA = {
    AcaoAuditoria.INSCRICAO_INDEFERIDA,
    AcaoAuditoria.INSCRICAO_CANCELADA,
    AcaoAuditoria.PRESENCA_AJUSTE_MANUAL,
    AcaoAuditoria.PRESENCA_REMOVIDA,
    AcaoAuditoria.CERTIFICADO_REEMITIDO,
    AcaoAuditoria.CERTIFICADO_CANCELADO,
}


class AuditoriaService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def registrar(
        self,
        acao: AcaoAuditoria,
        *,
        entidade: str,
        entidade_id: str | UUID,
        responsavel_id: UUID | None,
        evento_id: UUID | None = None,
        justificativa: str | None = None,
        dados: dict[str, Any] | None = None,
    ) -> LogAuditoria:
        if acao in ACOES_COM_JUSTIFICATIVA and not (justificativa and justificativa.strip()):
            raise RegraNegocioViolada("RN-10.1", "Esta ação exige uma justificativa.")

        log = LogAuditoria(
            acao=acao,
            entidade=entidade,
            entidade_id=str(entidade_id),
            responsavel_id=responsavel_id,
            evento_id=evento_id,
            justificativa=justificativa,
            dados=dados or {},
        )
        self.session.add(log)
        await self.session.flush()
        return log
