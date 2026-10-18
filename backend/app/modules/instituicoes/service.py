"""Regras de negócio de Instituição/Unidade (RF-002, UC02).

MÓDULO DE REFERÊNCIA: os demais módulos seguem esta divisão
router (HTTP) → service (regras, sem FastAPI) → repository (SQLAlchemy).
"""

from typing import Protocol
from uuid import UUID

from app.core.exceptions import Conflito, NaoEncontrado, RegraNegocioViolada
from app.modules.instituicoes.models import Instituicao, UnidadeOrganizadora
from app.modules.instituicoes.schemas import (
    InstituicaoAtualizar,
    InstituicaoCriar,
    UnidadeAtualizar,
    UnidadeCriar,
)


class InstituicaoRepositorio(Protocol):
    """Contrato usado pelo service — permite testar com um repositório falso."""

    async def listar(self, apenas_ativas: bool) -> list[Instituicao]: ...
    async def obter(self, instituicao_id: UUID) -> Instituicao | None: ...
    async def existe_nome(self, nome: str, ignorar_id: UUID | None = None) -> bool: ...
    async def adicionar(self, instituicao: Instituicao) -> Instituicao: ...
    async def salvar(self, instituicao: Instituicao) -> Instituicao: ...
    async def possui_evento_ativo(self, instituicao_id: UUID) -> bool: ...
    async def listar_unidades(self, instituicao_id: UUID) -> list[UnidadeOrganizadora]: ...
    async def obter_unidade(self, unidade_id: UUID) -> UnidadeOrganizadora | None: ...
    async def adicionar_unidade(self, unidade: UnidadeOrganizadora) -> UnidadeOrganizadora: ...
    async def salvar_unidade(self, unidade: UnidadeOrganizadora) -> UnidadeOrganizadora: ...
    async def unidade_possui_evento_ativo(self, unidade_id: UUID) -> bool: ...


class InstituicaoService:
    def __init__(self, repo: InstituicaoRepositorio):
        self.repo = repo

    async def listar(self, apenas_ativas: bool = False) -> list[Instituicao]:
        return await self.repo.listar(apenas_ativas)

    async def obter(self, instituicao_id: UUID) -> Instituicao:
        instituicao = await self.repo.obter(instituicao_id)
        if instituicao is None:
            raise NaoEncontrado("Instituição não encontrada.")
        return instituicao

    async def criar(self, dados: InstituicaoCriar) -> Instituicao:
        if await self.repo.existe_nome(dados.nome):
            raise Conflito("Já existe uma instituição com este nome.")
        return await self.repo.adicionar(
            Instituicao(nome=dados.nome, sigla=dados.sigla, dados=dados.dados, ativo=True)
        )

    async def atualizar(self, instituicao_id: UUID, dados: InstituicaoAtualizar) -> Instituicao:
        instituicao = await self.obter(instituicao_id)
        if dados.nome and await self.repo.existe_nome(dados.nome, ignorar_id=instituicao_id):
            raise Conflito("Já existe uma instituição com este nome.")
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(instituicao, campo, valor)
        return await self.repo.salvar(instituicao)

    async def inativar(self, instituicao_id: UUID) -> Instituicao:
        instituicao = await self.obter(instituicao_id)
        if await self.repo.possui_evento_ativo(instituicao_id):
            raise RegraNegocioViolada(
                "RN-1.1", "Instituição possui evento ativo vinculado e não pode ser inativada."
            )
        instituicao.ativo = False
        return await self.repo.salvar(instituicao)

    # --- unidades ---------------------------------------------------------

    async def listar_unidades(self, instituicao_id: UUID) -> list[UnidadeOrganizadora]:
        await self.obter(instituicao_id)
        return await self.repo.listar_unidades(instituicao_id)

    async def criar_unidade(self, instituicao_id: UUID, dados: UnidadeCriar) -> UnidadeOrganizadora:
        instituicao = await self.obter(instituicao_id)
        if not instituicao.ativo:
            raise RegraNegocioViolada(
                "RN-1.1", "Não é possível adicionar unidade a instituição inativa."
            )
        existentes = await self.repo.listar_unidades(instituicao_id)
        if any(u.nome.lower() == dados.nome.lower() for u in existentes):
            raise Conflito("Já existe uma unidade com este nome nesta instituição.")
        return await self.repo.adicionar_unidade(
            UnidadeOrganizadora(
                instituicao_id=instituicao_id, nome=dados.nome, tipo=dados.tipo, ativo=True
            )
        )

    async def atualizar_unidade(
        self, instituicao_id: UUID, unidade_id: UUID, dados: UnidadeAtualizar
    ) -> UnidadeOrganizadora:
        unidade = await self._obter_unidade(instituicao_id, unidade_id)
        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(unidade, campo, valor)
        return await self.repo.salvar_unidade(unidade)

    async def inativar_unidade(self, instituicao_id: UUID, unidade_id: UUID) -> UnidadeOrganizadora:
        unidade = await self._obter_unidade(instituicao_id, unidade_id)
        if await self.repo.unidade_possui_evento_ativo(unidade_id):
            raise RegraNegocioViolada(
                "RN-1.1", "Unidade possui evento ativo vinculado e não pode ser inativada."
            )
        unidade.ativo = False
        return await self.repo.salvar_unidade(unidade)

    async def _obter_unidade(self, instituicao_id: UUID, unidade_id: UUID) -> UnidadeOrganizadora:
        unidade = await self.repo.obter_unidade(unidade_id)
        if unidade is None or unidade.instituicao_id != instituicao_id:
            raise NaoEncontrado("Unidade organizadora não encontrada.")
        return unidade
