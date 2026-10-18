"""Módulo 6 — Pessoa/Participante (RF-005, UC05). RN 8.3, RNF-007/008.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Cadastro de pessoa e Meu perfil (Pedro) · Privacidade LGPD e Admin define perfil
— fora do MVP de 14/11.
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])
