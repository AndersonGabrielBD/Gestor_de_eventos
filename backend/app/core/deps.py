"""Dependências FastAPI de autenticação e autorização (RNF-006)."""

from collections.abc import Callable, Coroutine
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.perfis import Perfil, UsuarioAtual, perfil_atende
from app.core.security import TokenInvalido, decodificar_token

SessionDep = Annotated[AsyncSession, Depends(get_session)]

_bearer = HTTPBearer(auto_error=False)


async def get_usuario_atual(
    session: SessionDep,
    credenciais: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> UsuarioAtual:
    if credenciais is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token ausente")
    try:
        claims = decodificar_token(credenciais.credentials)
    except TokenInvalido as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token inválido ou expirado") from exc

    user_id = UUID(claims["sub"])
    linha = (
        await session.execute(
            text(
                "select id, perfil, consentimento_lgpd_em is not null as completo"
                " from public.pessoa where user_id = :uid"
            ),
            {"uid": user_id},
        )
    ).first()

    return UsuarioAtual(
        user_id=user_id,
        email=claims.get("email"),
        pessoa_id=linha.id if linha else None,
        perfil=Perfil(linha.perfil) if linha else Perfil.PARTICIPANTE,
        cadastro_completo=bool(linha and linha.completo),
    )


UsuarioDep = Annotated[UsuarioAtual, Depends(get_usuario_atual)]


def require_perfil(
    minimo: Perfil,
) -> Callable[[UsuarioAtual], Coroutine[Any, Any, UsuarioAtual]]:
    """Uso: `usuario: UsuarioAtual = Depends(require_perfil(Perfil.ADMINISTRADOR))`."""

    async def _verificar(usuario: UsuarioDep) -> UsuarioAtual:
        if not perfil_atende(usuario.perfil, minimo):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Perfil sem permissão para esta ação")
        return usuario

    return _verificar


AdminDep = Annotated[UsuarioAtual, Depends(require_perfil(Perfil.ADMINISTRADOR))]
CoordenadorDep = Annotated[UsuarioAtual, Depends(require_perfil(Perfil.COORDENADOR))]
