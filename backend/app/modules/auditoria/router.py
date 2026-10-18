"""Módulo 10 — Consulta de auditoria (RF-011, UC11, tela T05).

O registro já está pronto em `service.py`. Falta a consulta/exportação.
Backlog: GE-082, GE-083, GE-085.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auditoria", tags=["Auditoria"])
