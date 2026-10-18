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
    pessoa_id: UUID | None  # nulo enquanto o cadastro da pessoa não foi completado
    perfil: Perfil

    @property
    def eh_admin(self) -> bool:
        return self.perfil == Perfil.ADMINISTRADOR
