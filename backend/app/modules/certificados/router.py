"""Módulo 9 — Tipos de certificado e Certificados (RF-009/010, UC09/10/15).

Telas: T04, T12, T16, T17.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Backlog: GE-100 a GE-10F — ver docs/BACKLOG.md e docs/05-api.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Certificados"])
