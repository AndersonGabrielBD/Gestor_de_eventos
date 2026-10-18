"""Testes unitários do service de referência, usando um repositório em memória."""

from uuid import UUID, uuid4

import pytest

from app.core.exceptions import Conflito, NaoEncontrado, RegraNegocioViolada
from app.modules.instituicoes.models import Instituicao, UnidadeOrganizadora
from app.modules.instituicoes.schemas import (
    InstituicaoAtualizar,
    InstituicaoCriar,
    UnidadeCriar,
)
from app.modules.instituicoes.service import InstituicaoService


class RepositorioEmMemoria:
    def __init__(self):
        self.instituicoes: dict[UUID, Instituicao] = {}
        self.unidades: dict[UUID, UnidadeOrganizadora] = {}
        self.com_evento_ativo: set[UUID] = set()  # ids de instituições/unidades

    async def listar(self, apenas_ativas):
        return [i for i in self.instituicoes.values() if i.ativo or not apenas_ativas]

    async def obter(self, instituicao_id):
        return self.instituicoes.get(instituicao_id)

    async def existe_nome(self, nome, ignorar_id=None):
        return any(
            i.nome.lower() == nome.lower() and i.id != ignorar_id
            for i in self.instituicoes.values()
        )

    async def adicionar(self, instituicao):
        instituicao.id = uuid4()
        self.instituicoes[instituicao.id] = instituicao
        return instituicao

    async def salvar(self, instituicao):
        return instituicao

    async def possui_evento_ativo(self, instituicao_id):
        return instituicao_id in self.com_evento_ativo

    async def listar_unidades(self, instituicao_id):
        return [u for u in self.unidades.values() if u.instituicao_id == instituicao_id]

    async def obter_unidade(self, unidade_id):
        return self.unidades.get(unidade_id)

    async def adicionar_unidade(self, unidade):
        unidade.id = uuid4()
        self.unidades[unidade.id] = unidade
        return unidade

    async def salvar_unidade(self, unidade):
        return unidade

    async def unidade_possui_evento_ativo(self, unidade_id):
        return unidade_id in self.com_evento_ativo


@pytest.fixture
def repo():
    return RepositorioEmMemoria()


@pytest.fixture
def service(repo):
    return InstituicaoService(repo)


async def test_cria_instituicao_ativa(service):
    inst = await service.criar(InstituicaoCriar(nome="Centro Universitário X", sigla="CUX"))
    assert inst.ativo is True
    assert inst.sigla == "CUX"


async def test_nome_duplicado_gera_conflito(service):
    await service.criar(InstituicaoCriar(nome="Centro Universitário X"))
    with pytest.raises(Conflito):
        await service.criar(InstituicaoCriar(nome="centro universitário x"))


async def test_atualiza_somente_campos_enviados(service):
    inst = await service.criar(InstituicaoCriar(nome="Original", sigla="ORG"))
    atualizada = await service.atualizar(inst.id, InstituicaoAtualizar(nome="Novo nome"))
    assert atualizada.nome == "Novo nome"
    assert atualizada.sigla == "ORG"


async def test_obter_inexistente(service):
    with pytest.raises(NaoEncontrado):
        await service.obter(uuid4())


async def test_rn_1_1_bloqueia_inativar_instituicao_com_evento_ativo(service, repo):
    inst = await service.criar(InstituicaoCriar(nome="Com evento"))
    repo.com_evento_ativo.add(inst.id)
    with pytest.raises(RegraNegocioViolada) as erro:
        await service.inativar(inst.id)
    assert erro.value.codigo == "RN-1.1"
    assert inst.ativo is True


async def test_inativa_instituicao_sem_evento_ativo(service):
    inst = await service.criar(InstituicaoCriar(nome="Sem evento"))
    assert (await service.inativar(inst.id)).ativo is False


async def test_rn_1_1_bloqueia_inativar_unidade_com_evento_ativo(service, repo):
    inst = await service.criar(InstituicaoCriar(nome="Inst"))
    unidade = await service.criar_unidade(inst.id, UnidadeCriar(nome="Curso A"))
    repo.com_evento_ativo.add(unidade.id)
    with pytest.raises(RegraNegocioViolada):
        await service.inativar_unidade(inst.id, unidade.id)


async def test_nao_adiciona_unidade_em_instituicao_inativa(service):
    inst = await service.criar(InstituicaoCriar(nome="Inst"))
    await service.inativar(inst.id)
    with pytest.raises(RegraNegocioViolada):
        await service.criar_unidade(inst.id, UnidadeCriar(nome="Curso A"))


async def test_unidade_de_outra_instituicao_nao_e_encontrada(service):
    a = await service.criar(InstituicaoCriar(nome="Inst A"))
    b = await service.criar(InstituicaoCriar(nome="Inst B"))
    unidade = await service.criar_unidade(a.id, UnidadeCriar(nome="Curso"))
    with pytest.raises(NaoEncontrado):
        await service.inativar_unidade(b.id, unidade.id)
