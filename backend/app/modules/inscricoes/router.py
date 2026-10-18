"""Módulo 7 — Inscrição e Status (RF-006/007, UC06/07/13/14, telas T10, T13–T15).

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Backlog: GE-070 a GE-07C — ver docs/BACKLOG.md e docs/05-api.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Inscrições"])
