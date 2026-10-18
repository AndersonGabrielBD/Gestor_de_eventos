from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TipoUnidade(StrEnum):
    CAMPUS = "campus"
    CENTRO = "centro"
    CURSO = "curso"
    OUTRO = "outro"


class Instituicao(Base):
    __tablename__ = "instituicao"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    nome: Mapped[str] = mapped_column(Text)
    sigla: Mapped[str | None] = mapped_column(Text)
    dados: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict)
    ativo: Mapped[bool] = mapped_column(default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class UnidadeOrganizadora(Base):
    __tablename__ = "unidade_organizadora"

    id: Mapped[UUID] = mapped_column(primary_key=True, server_default=func.gen_random_uuid())
    instituicao_id: Mapped[UUID] = mapped_column(ForeignKey("instituicao.id"))
    nome: Mapped[str] = mapped_column(Text)
    tipo: Mapped[TipoUnidade] = mapped_column(
        ENUM(
            TipoUnidade,
            name="tipo_unidade",
            create_type=False,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=TipoUnidade.CURSO,
    )
    ativo: Mapped[bool] = mapped_column(default=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
