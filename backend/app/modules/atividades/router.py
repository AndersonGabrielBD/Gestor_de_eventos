"""Módulo 5 — Atividade (RF-004, UC04, tela T09). RN 1.3, 1.4, 5.4.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Programação / Atividades (Pedro).
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Atividades"])
