from app.core.perfis import Perfil, perfil_atende


async def test_health(client):
    resposta = await client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


async def test_rota_protegida_sem_token_retorna_401(client):
    resposta = await client.get("/api/v1/auth/me")
    assert resposta.status_code == 401


async def test_auth_me_retorna_perfil(client, logar_como):
    usuario = logar_como(Perfil.COORDENADOR)
    resposta = await client.get("/api/v1/auth/me")
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["perfil"] == "coordenador"
    assert corpo["pessoa_id"] == str(usuario.pessoa_id)


async def test_participante_nao_cria_instituicao(client, logar_como):
    logar_como(Perfil.PARTICIPANTE)
    resposta = await client.post("/api/v1/instituicoes", json={"nome": "Nova Instituição"})
    assert resposta.status_code == 403


def test_hierarquia_de_perfis():
    assert perfil_atende(Perfil.ADMINISTRADOR, Perfil.COORDENADOR)
    assert perfil_atende(Perfil.COORDENADOR, Perfil.PARTICIPANTE)
    assert not perfil_atende(Perfil.COORDENADOR, Perfil.ADMINISTRADOR)
    assert not perfil_atende(Perfil.PARTICIPANTE, Perfil.COORDENADOR)
