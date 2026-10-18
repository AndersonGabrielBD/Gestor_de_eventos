"""Módulo 7 — Inscrição e Status (RF-006/007, UC06/07/13/14, telas T10, T13–T15).

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Tela de inscrição (Thayná) · Minhas inscrições e Gestão de inscritos (Pedro).
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Inscrições"])
