from uuid import UUID

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.instituicoes.models import Instituicao, UnidadeOrganizadora

# "Evento ativo" = qualquer evento ainda não encerrado (RN 1.1).
_SQL_EVENTO_ATIVO_INSTITUICAO = text(
    """
    select exists (
        select 1 from public.evento e
        join public.unidade_organizadora u on u.id = e.unidade_organizadora_id
        where u.instituicao_id = :id and e.status <> 'encerrado'
    )
    """
)
_SQL_EVENTO_ATIVO_UNIDADE = text(
    """
    select exists (
        select 1 from public.evento e
        where e.unidade_organizadora_id = :id and e.status <> 'encerrado'
    )
    """
)


class InstituicaoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def listar(self, apenas_ativas: bool) -> list[Instituicao]:
        consulta = select(Instituicao).order_by(Instituicao.nome)
        if apenas_ativas:
            consulta = consulta.where(Instituicao.ativo.is_(True))
        return list((await self.session.scalars(consulta)).all())

    async def obter(self, instituicao_id: UUID) -> Instituicao | None:
        return await self.session.get(Instituicao, instituicao_id)

    async def existe_nome(self, nome: str, ignorar_id: UUID | None = None) -> bool:
        consulta = select(Instituicao.id).where(func.lower(Instituicao.nome) == nome.lower())
        if ignorar_id:
            consulta = consulta.where(Instituicao.id != ignorar_id)
        return (await self.session.scalar(consulta)) is not None

    async def adicionar(self, instituicao: Instituicao) -> Instituicao:
        self.session.add(instituicao)
        await self.session.flush()
        await self.session.refresh(instituicao)
        return instituicao

    async def salvar(self, instituicao: Instituicao) -> Instituicao:
        await self.session.flush()
        await self.session.refresh(instituicao)
        return instituicao

    async def possui_evento_ativo(self, instituicao_id: UUID) -> bool:
        return bool(
            await self.session.scalar(_SQL_EVENTO_ATIVO_INSTITUICAO, {"id": instituicao_id})
        )

    # --- unidades ---------------------------------------------------------

    async def listar_unidades(self, instituicao_id: UUID) -> list[UnidadeOrganizadora]:
        consulta = (
            select(UnidadeOrganizadora)
            .where(UnidadeOrganizadora.instituicao_id == instituicao_id)
            .order_by(UnidadeOrganizadora.nome)
        )
        return list((await self.session.scalars(consulta)).all())

    async def obter_unidade(self, unidade_id: UUID) -> UnidadeOrganizadora | None:
        return await self.session.get(UnidadeOrganizadora, unidade_id)

    async def adicionar_unidade(self, unidade: UnidadeOrganizadora) -> UnidadeOrganizadora:
        self.session.add(unidade)
        await self.session.flush()
        await self.session.refresh(unidade)
        return unidade

    async def salvar_unidade(self, unidade: UnidadeOrganizadora) -> UnidadeOrganizadora:
        await self.session.flush()
        await self.session.refresh(unidade)
        return unidade

    async def unidade_possui_evento_ativo(self, unidade_id: UUID) -> bool:
        return bool(await self.session.scalar(_SQL_EVENTO_ATIVO_UNIDADE, {"id": unidade_id}))
