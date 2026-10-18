"""Módulo 9 — Tipos de certificado e Certificados (RF-009/010, UC09/10/15).

Telas: T04, T12, T16, T17.

A implementar seguindo o módulo de referência `app/modules/instituicoes`
(models.py → schemas.py → repository.py → service.py → router.py).
Cards no Trello: Apuração e Emissão em lote (José) · Meus certificados e validação (Thayná).
Tipos de certificado (vêm do seed) e Reemissão ficaram fora do MVP de 14/11.
Ver docs/BACKLOG.md e docs/08-dependencias.md.
"""

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["Certificados"])
