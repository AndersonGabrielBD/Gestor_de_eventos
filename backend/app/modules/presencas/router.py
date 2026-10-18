"""Módulo 8 — Presença/Participação (RF-008, UC08, tela T11). RN 4.x, 10.2.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Check-in e presença (Anderson).
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Presença"])
