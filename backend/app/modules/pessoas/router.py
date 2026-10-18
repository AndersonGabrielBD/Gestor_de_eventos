"""Módulo 6 — Pessoa/Participante (RF-005, UC05). RN 8.3, RNF-007/008.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Backlog: GE-060 a GE-065, GE-121, GE-122 — ver docs/BACKLOG.md e docs/05-api.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/pessoas", tags=["Pessoas"])
