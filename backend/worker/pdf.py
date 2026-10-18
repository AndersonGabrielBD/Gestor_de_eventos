"""Geração do PDF do certificado (RNF-010, RN 6.1/6.2). Backlog: GE-106.

Pipeline: template HTML → WeasyPrint (PDF) → QR Code embutido → pikepdf (metadados
PDF/A) → SHA-256 do arquivo. As importações ficam dentro das funções porque
WeasyPrint exige bibliotecas de sistema (Pango) disponíveis só no container do worker.
"""

import base64
import hashlib
import io
from dataclasses import dataclass


@dataclass(frozen=True)
class DadosCertificado:
    codigo: str
    versao: int
    nome: str
    evento: str
    tipo: str
    carga_horaria: float
    data_emissao: str
    url_validacao: str


def gerar_qr_code_png(conteudo: str) -> bytes:
    import qrcode

    buffer = io.BytesIO()
    qrcode.make(conteudo).save(buffer, format="PNG")
    return buffer.getvalue()


def montar_html(dados: DadosCertificado) -> str:
    """TODO (GE-106): mover para um template Jinja2 com a identidade visual da instituição."""
    qr = base64.b64encode(gerar_qr_code_png(dados.url_validacao)).decode()
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Certificado {dados.codigo}</title>
<style>@page {{ size: A4 landscape; margin: 2cm; }} body {{ font-family: sans-serif; }}</style>
</head><body>
<h1>Certificado</h1>
<p>Certificamos que <strong>{dados.nome}</strong> participou do evento
<strong>{dados.evento}</strong> na condição de <strong>{dados.tipo}</strong>,
com carga horária de <strong>{dados.carga_horaria:g} horas</strong>.</p>
<p>Emitido em {dados.data_emissao}. Código de verificação: {dados.codigo} (v{dados.versao})</p>
<img alt="QR Code de validação" src="data:image/png;base64,{qr}" width="120">
</body></html>"""


def gerar_certificado_pdf(dados: DadosCertificado) -> tuple[bytes, str]:
    """Retorna (bytes do PDF, sha256). TODO (GE-106): conformidade PDF/A-2b completa
    (perfil ICC sRGB + XMP) com pikepdf e validação com veraPDF."""
    from weasyprint import HTML

    pdf = HTML(string=montar_html(dados)).write_pdf(pdf_variant="pdf/a-2b")
    return pdf, hashlib.sha256(pdf).hexdigest()
