"""Módulo 11 — Relatórios (RF-012, UC12, tela T06). RN 10.3.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Relatórios oficiais e Dashboard por perfil — fora do MVP de 14/11.
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])
