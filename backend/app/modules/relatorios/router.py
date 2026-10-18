"""Módulo 11 — Relatórios (RF-012, UC12, tela T06). RN 10.3.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Backlog: GE-110 a GE-114 — ver docs/BACKLOG.md e docs/05-api.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])
