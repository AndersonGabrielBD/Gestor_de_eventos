from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.instituicoes.models import TipoUnidade


class InstituicaoCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=200)
    sigla: str | None = Field(default=None, max_length=20)
    dados: dict[str, Any] = Field(default_factory=dict, description="CNPJ, endereço, contato…")


class InstituicaoAtualizar(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=200)
    sigla: str | None = Field(default=None, max_length=20)
    dados: dict[str, Any] | None = None


class InstituicaoLeitura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    sigla: str | None
    dados: dict[str, Any]
    ativo: bool
    criado_em: datetime


class UnidadeCriar(BaseModel):
    nome: str = Field(min_length=2, max_length=200)
    tipo: TipoUnidade = TipoUnidade.CURSO


class UnidadeAtualizar(BaseModel):
    nome: str | None = Field(default=None, min_length=2, max_length=200)
    tipo: TipoUnidade | None = None


class UnidadeLeitura(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    instituicao_id: UUID
    nome: str
    tipo: TipoUnidade
    ativo: bool
