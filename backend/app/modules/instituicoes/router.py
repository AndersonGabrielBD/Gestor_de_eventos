"""Endpoints de Instituição/Unidade (UC02, tela T03)."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.deps import AdminDep, SessionDep, UsuarioDep
from app.modules.instituicoes.repository import InstituicaoRepository
from app.modules.instituicoes.schemas import (
    InstituicaoAtualizar,
    InstituicaoCriar,
    InstituicaoLeitura,
    UnidadeAtualizar,
    UnidadeCriar,
    UnidadeLeitura,
)
from app.modules.instituicoes.service import InstituicaoService

router = APIRouter(prefix="/instituicoes", tags=["Instituições"])


def get_service(session: SessionDep) -> InstituicaoService:
    return InstituicaoService(InstituicaoRepository(session))


ServiceDep = Annotated[InstituicaoService, Depends(get_service)]


@router.get("", response_model=list[InstituicaoLeitura])
async def listar(_: UsuarioDep, service: ServiceDep, apenas_ativas: bool = False):
    return await service.listar(apenas_ativas)


@router.post("", response_model=InstituicaoLeitura, status_code=status.HTTP_201_CREATED)
async def criar(dados: InstituicaoCriar, _: AdminDep, service: ServiceDep):
    return await service.criar(dados)


@router.get("/{instituicao_id}", response_model=InstituicaoLeitura)
async def obter(instituicao_id: UUID, _: UsuarioDep, service: ServiceDep):
    return await service.obter(instituicao_id)


@router.put("/{instituicao_id}", response_model=InstituicaoLeitura)
async def atualizar(
    instituicao_id: UUID, dados: InstituicaoAtualizar, _: AdminDep, service: ServiceDep
):
    return await service.atualizar(instituicao_id, dados)


@router.post("/{instituicao_id}/inativar", response_model=InstituicaoLeitura)
async def inativar(instituicao_id: UUID, _: AdminDep, service: ServiceDep):
    return await service.inativar(instituicao_id)


@router.get("/{instituicao_id}/unidades", response_model=list[UnidadeLeitura])
async def listar_unidades(instituicao_id: UUID, _: UsuarioDep, service: ServiceDep):
    return await service.listar_unidades(instituicao_id)


@router.post(
    "/{instituicao_id}/unidades",
    response_model=UnidadeLeitura,
    status_code=status.HTTP_201_CREATED,
)
async def criar_unidade(
    instituicao_id: UUID, dados: UnidadeCriar, _: AdminDep, service: ServiceDep
):
    return await service.criar_unidade(instituicao_id, dados)


@router.put("/{instituicao_id}/unidades/{unidade_id}", response_model=UnidadeLeitura)
async def atualizar_unidade(
    instituicao_id: UUID,
    unidade_id: UUID,
    dados: UnidadeAtualizar,
    _: AdminDep,
    service: ServiceDep,
):
    return await service.atualizar_unidade(instituicao_id, unidade_id, dados)


@router.post("/{instituicao_id}/unidades/{unidade_id}/inativar", response_model=UnidadeLeitura)
async def inativar_unidade(
    instituicao_id: UUID, unidade_id: UUID, _: AdminDep, service: ServiceDep
):
    return await service.inativar_unidade(instituicao_id, unidade_id)
