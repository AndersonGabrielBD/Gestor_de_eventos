"""Cria (ou atualiza) um usuário de teste de cada perfil no projeto Supabase do .env.

Uso, dentro de backend/ com o venv ativo:

    python -m scripts.criar_usuarios_teste

Precisa de SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY e DATABASE_URL no .env.
A senha vem de SENHA_USUARIOS_TESTE (no .env ou no ambiente); se não estiver definida,
o script gera uma e mostra no terminal. Compartilhe com a equipe por canal seguro.
Só para o projeto de desenvolvimento — nunca rode em produção.
"""

import asyncio
import os
import secrets

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import get_settings

USUARIOS = [
    ("admin.teste@gestor-eventos.dev", "Admin de Teste", "administrador", "tecnico"),
    ("coordenador.teste@gestor-eventos.dev", "Coordenadora de Teste", "coordenador", "docente"),
    ("participante.teste@gestor-eventos.dev", "Participante de Teste", "participante", "discente"),
]


def senha_de_teste() -> str:
    senha = os.environ.get("SENHA_USUARIOS_TESTE")
    if not senha:
        from dotenv import dotenv_values  # vem com pydantic-settings

        senha = dotenv_values(".env").get("SENHA_USUARIOS_TESTE")
    return senha or f"Teste{secrets.token_hex(4)}"


def criar_conta(cliente: httpx.Client, email: str, nome: str, senha: str) -> None:
    resposta = cliente.post(
        "/auth/v1/admin/users",
        json={
            "email": email,
            "password": senha,
            "email_confirm": True,
            "user_metadata": {"nome": nome},
        },
    )
    if resposta.status_code == 422 and "email_exists" in resposta.text:
        print(f"  já existia: {email}")
        return
    resposta.raise_for_status()
    print(f"  criada: {email}")


async def ajustar_pessoas(database_url: str) -> None:
    """O trigger criou as pessoas como participante; aqui ajusta perfil, categoria e aceite."""
    engine = create_async_engine(database_url, connect_args={"statement_cache_size": 0})
    async with engine.begin() as conexao:
        for email, _nome, perfil, categoria in USUARIOS:
            resultado = await conexao.execute(
                text(
                    "update public.pessoa set perfil = cast(:perfil as perfil_usuario),"
                    " categoria = cast(:categoria as categoria_pessoa),"
                    " consentimento_lgpd_em = coalesce(consentimento_lgpd_em, now())"
                    " where email = :email"
                ),
                {"perfil": perfil, "categoria": categoria, "email": email},
            )
            if resultado.rowcount == 0:
                print(f"  ⚠️ pessoa não encontrada para {email} — a migration do trigger rodou?")
    await engine.dispose()


def main() -> None:
    settings = get_settings()
    if not settings.supabase_service_role_key:
        raise SystemExit("Preencha SUPABASE_SERVICE_ROLE_KEY no backend/.env")

    senha = senha_de_teste()
    chave = settings.supabase_service_role_key
    with httpx.Client(
        base_url=settings.supabase_url,
        headers={"apikey": chave, "Authorization": f"Bearer {chave}"},
        timeout=30,
    ) as cliente:
        print("Contas:")
        for email, nome, _perfil, _categoria in USUARIOS:
            criar_conta(cliente, email, nome, senha)

    print("Perfis:")
    asyncio.run(ajustar_pessoas(settings.database_url))

    print("\nPronto. Usuários de teste:")
    for email, _nome, perfil, _categoria in USUARIOS:
        print(f"  {perfil:<14} {email}")
    if "SENHA_USUARIOS_TESTE" not in os.environ:
        print(f"Senha de todos: {senha}  (guarde e envie por canal seguro)")


if __name__ == "__main__":
    main()
