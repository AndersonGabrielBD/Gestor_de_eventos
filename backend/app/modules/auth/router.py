"""UC00 — o login em si é feito pelo Supabase Auth no frontend (ADR-02)."""

from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.deps import UsuarioDep
from app.core.perfis import Perfil

router = APIRouter(prefix="/auth", tags=["Autenticação"])


class Eu(BaseModel):
    user_id: UUID
    email: str | None
    pessoa_id: UUID | None
    perfil: Perfil
    cadastro_completo: bool


@router.get("/me", response_model=Eu)
async def me(usuario: UsuarioDep) -> Eu:
    return Eu(
        user_id=usuario.user_id,
        email=usuario.email,
        pessoa_id=usuario.pessoa_id,
        perfil=usuario.perfil,
        cadastro_completo=usuario.cadastro_completo,
    )
