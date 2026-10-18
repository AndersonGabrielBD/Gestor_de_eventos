from collections.abc import AsyncIterator, Callable
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.deps import get_usuario_atual
from app.core.perfis import Perfil, UsuarioAtual
from app.main import app


def usuario_fake(perfil: Perfil) -> UsuarioAtual:
    return UsuarioAtual(
        user_id=uuid4(), email="teste@exemplo.com", pessoa_id=uuid4(), perfil=perfil
    )


@pytest.fixture
async def client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://teste") as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def logar_como() -> Callable[[Perfil], UsuarioAtual]:
    """Substitui a autenticação real por um usuário com o perfil informado."""

    def _logar(perfil: Perfil) -> UsuarioAtual:
        usuario = usuario_fake(perfil)
        app.dependency_overrides[get_usuario_atual] = lambda: usuario
        return usuario

    return _logar
