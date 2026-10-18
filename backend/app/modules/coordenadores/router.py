"""Módulo 4 — Coordenador do Evento (RF-003, UC03, tela T08). RN 1.2.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Backlog: GE-035, GE-039 — ver docs/BACKLOG.md e docs/05-api.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/eventos", tags=["Coordenadores"])
