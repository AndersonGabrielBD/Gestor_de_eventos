"""Validação do JWT emitido pelo Supabase Auth (ADR-02)."""

from functools import lru_cache
from typing import Any

import jwt

from app.core.config import get_settings

AUDIENCIA = "authenticated"


class TokenInvalido(Exception):
    pass


@lru_cache
def _jwks_client() -> jwt.PyJWKClient:
    return jwt.PyJWKClient(get_settings().jwks_url, cache_keys=True)


def decodificar_token(token: str) -> dict[str, Any]:
    """Retorna as claims do token. Usa o segredo HS256 se configurado; caso contrário,
    busca a chave pública no JWKS do projeto Supabase."""
    settings = get_settings()
    try:
        if settings.supabase_jwt_secret:
            return jwt.decode(
                token, settings.supabase_jwt_secret, algorithms=["HS256"], audience=AUDIENCIA
            )
        chave = _jwks_client().get_signing_key_from_jwt(token)
        return jwt.decode(token, chave.key, algorithms=["RS256", "ES256"], audience=AUDIENCIA)
    except jwt.PyJWTError as exc:
        raise TokenInvalido(str(exc)) from exc
