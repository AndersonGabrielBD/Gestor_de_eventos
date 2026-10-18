"""Módulo 3 — Evento (RF-001, UC01, tela T07).

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Backlog: GE-030 a GE-038 — ver docs/BACKLOG.md e docs/05-api.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/eventos", tags=["Eventos"])
