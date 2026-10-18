from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Identity, Text, func
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AcaoAuditoria(StrEnum):
    INSCRICAO_STATUS_ALTERADO = "inscricao_status_alterado"
    INSCRICAO_INDEFERIDA = "inscricao_indeferida"
    INSCRICAO_CANCELADA = "inscricao_cancelada"
    PRESENCA_AJUSTE_MANUAL = "presenca_ajuste_manual"
    PRESENCA_REMOVIDA = "presenca_removida"
    CERTIFICADO_EMITIDO = "certificado_emitido"
    CERTIFICADO_REEMITIDO = "certificado_reemitido"
    CERTIFICADO_CANCELADO = "certificado_cancelado"
    EVENTO_STATUS_ALTERADO = "evento_status_alterado"
    COORDENADOR_VINCULADO = "coordenador_vinculado"
    COORDENADOR_REMOVIDO = "coordenador_removido"
    PERFIL_ALTERADO = "perfil_alterado"
    PESSOA_ANONIMIZADA = "pessoa_anonimizada"


class LogAuditoria(Base):
    """Tabela append-only: o banco rejeita UPDATE/DELETE (trigger)."""

    __tablename__ = "log_auditoria"

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    acao: Mapped[AcaoAuditoria] = mapped_column(
        ENUM(
            AcaoAuditoria,
            name="acao_auditoria",
            create_type=False,
            values_callable=lambda e: [m.value for m in e],
        )
    )
    responsavel_id: Mapped[UUID | None]
    evento_id: Mapped[UUID | None]
    entidade: Mapped[str] = mapped_column(Text)
    entidade_id: Mapped[str] = mapped_column(Text)
    justificativa: Mapped[str | None] = mapped_column(Text)
    dados: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
