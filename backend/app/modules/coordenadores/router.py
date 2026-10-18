"""Módulo 4 — Coordenador do Evento (RF-003, UC03, tela T08). RN 1.2.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Coordenadores do evento — fora do MVP de 14/11
(quem cria o evento é o coordenador).
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/eventos", tags=["Coordenadores"])
