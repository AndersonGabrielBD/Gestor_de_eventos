from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class Perfil(StrEnum):
    PARTICIPANTE = "participante"
    COORDENADOR = "coordenador"
    ADMINISTRADOR = "administrador"


# Hierarquia: administrador herda coordenador, que herda participante (seção 5.1 do doc).
_NIVEL = {Perfil.PARTICIPANTE: 0, Perfil.COORDENADOR: 1, Perfil.ADMINISTRADOR: 2}


def perfil_atende(perfil: Perfil, minimo: Perfil) -> bool:
    return _NIVEL[perfil] >= _NIVEL[minimo]


@dataclass(frozen=True)
class UsuarioAtual:
    user_id: UUID
    email: str | None
    pessoa_id: UUID | None  # criada por trigger no cadastro da conta; nula só se o trigger falhou
    perfil: Perfil
    # Completou "Meu perfil" (dados + aceite LGPD). Sem isso não pode se inscrever.
    cadastro_completo: bool = False

    @property
    def eh_admin(self) -> bool:
        return self.perfil == Perfil.ADMINISTRADOR
