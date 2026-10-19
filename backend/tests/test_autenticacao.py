"""Card "Login, cadastro e recuperação de senha": validação do JWT do Supabase e perfis."""

import time
from collections import namedtuple
from uuid import uuid4

import jwt
import pytest

from app.core.config import get_settings
from app.core.database import get_session
from app.core.perfis import Perfil
from app.core.security import TokenInvalido, decodificar_token
from app.main import app

SEGREDO = "segredo-de-teste-com-pelo-menos-32-bytes!!"
LinhaPessoa = namedtuple("LinhaPessoa", "id perfil completo")


def gerar_token(segredo: str = SEGREDO, **claims) -> str:
    agora = int(time.time())
    payload = {
        "sub": str(uuid4()),
        "email": "pessoa@exemplo.com",
        "aud": "authenticated",
        "iat": agora,
        "exp": agora + 3600,
    } | claims
    return jwt.encode(payload, segredo, algorithm="HS256")


@pytest.fixture(autouse=True)
def segredo_hs256(monkeypatch):
    monkeypatch.setattr(get_settings(), "supabase_jwt_secret", SEGREDO)


class SessaoFalsa:
    """Responde à consulta da pessoa feita em get_usuario_atual."""

    def __init__(self, linha: LinhaPessoa | None):
        self.linha = linha

    async def execute(self, *_args, **_kwargs):
        return self

    def first(self):
        return self.linha


def usar_pessoa(linha: LinhaPessoa | None) -> None:
    async def _sessao():
        yield SessaoFalsa(linha)

    app.dependency_overrides[get_session] = _sessao


# --- decodificar_token -------------------------------------------------------


def test_token_valido_retorna_claims():
    claims = decodificar_token(gerar_token(email="a@b.com"))
    assert claims["email"] == "a@b.com"


@pytest.mark.parametrize(
    "token",
    [
        pytest.param(gerar_token(exp=int(time.time()) - 10), id="expirado"),
        pytest.param(
            gerar_token(segredo="outro-segredo-com-pelo-menos-32-bytes!!"), id="assinatura"
        ),
        pytest.param(gerar_token(aud="anon"), id="audiencia"),
        pytest.param("isto-nao-e-um-jwt", id="malformado"),
    ],
)
def test_token_rejeitado(token):
    with pytest.raises(TokenInvalido):
        decodificar_token(token)


# --- API ---------------------------------------------------------------------


@pytest.mark.parametrize(
    "token",
    [gerar_token(exp=int(time.time()) - 10), "isto-nao-e-um-jwt"],
    ids=["expirado", "malformado"],
)
async def test_token_invalido_retorna_401(client, token):
    resposta = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resposta.status_code == 401


async def test_auth_me_com_token_real(client):
    pessoa_id = uuid4()
    usar_pessoa(LinhaPessoa(pessoa_id, "coordenador", False))

    resposta = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {gerar_token()}"}
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["pessoa_id"] == str(pessoa_id)
    assert corpo["perfil"] == "coordenador"
    assert corpo["cadastro_completo"] is False


async def test_cadastro_completo_quando_aceitou_termo(client):
    usar_pessoa(LinhaPessoa(uuid4(), "participante", True))
    resposta = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {gerar_token()}"}
    )
    assert resposta.json()["cadastro_completo"] is True


async def test_sem_pessoa_vira_participante(client):
    usar_pessoa(None)
    resposta = await client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {gerar_token()}"}
    )
    corpo = resposta.json()
    assert corpo["perfil"] == "participante"
    assert corpo["pessoa_id"] is None


async def test_coordenador_nao_acessa_rota_de_admin(client, logar_como):
    logar_como(Perfil.COORDENADOR)
    resposta = await client.post("/api/v1/instituicoes", json={"nome": "Nova Instituição"})
    assert resposta.status_code == 403
