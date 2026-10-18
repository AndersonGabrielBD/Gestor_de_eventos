"""Módulo 11 — Relatórios (RF-012, UC12, tela T06). RN 10.3.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Relatórios oficiais (Pedro) · Dashboard por perfil (Anderson).
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])
