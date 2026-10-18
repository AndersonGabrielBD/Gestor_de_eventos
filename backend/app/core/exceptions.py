"""Exceções de domínio. Python puro: os services lançam estas exceções sem depender
do FastAPI; `app.main` as converte em respostas HTTP."""


class ErroDominio(Exception):
    status_code = 400
    codigo = "ERRO"

    def __init__(self, mensagem: str, codigo: str | None = None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        if codigo:
            self.codigo = codigo


class NaoEncontrado(ErroDominio):
    status_code = 404
    codigo = "NAO_ENCONTRADO"


class RegraNegocioViolada(ErroDominio):
    """Use o código da RN, ex.: RegraNegocioViolada("RN-1.1", "...")."""

    status_code = 422

    def __init__(self, codigo_rn: str, mensagem: str):
        super().__init__(mensagem, codigo_rn)


class Conflito(ErroDominio):
    status_code = 409
    codigo = "CONFLITO"


class AcessoNegado(ErroDominio):
    status_code = 403
    codigo = "ACESSO_NEGADO"
