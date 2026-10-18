"""Módulo 3 — Evento (RF-001, UC01, tela T07).

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Criar e gerenciar evento (Anderson).
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/eventos", tags=["Eventos"])
