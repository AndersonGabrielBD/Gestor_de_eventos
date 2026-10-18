from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import ErroDominio
from app.modules.atividades.router import router as atividades_router
from app.modules.auditoria.router import router as auditoria_router
from app.modules.auth.router import router as auth_router
from app.modules.certificados.router import router as certificados_router
from app.modules.coordenadores.router import router as coordenadores_router
from app.modules.eventos.router import router as eventos_router
from app.modules.inscricoes.router import router as inscricoes_router
from app.modules.instituicoes.router import router as instituicoes_router
from app.modules.pessoas.router import router as pessoas_router
from app.modules.presencas.router import router as presencas_router
from app.modules.relatorios.router import router as relatorios_router

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Gestão de Eventos Institucionais — API",
        version="0.1.0",
        docs_url="/docs",
        openapi_url=f"{API_PREFIX}/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(ErroDominio)
    async def _erro_dominio(_: Request, exc: ErroDominio) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"codigo": exc.codigo, "mensagem": exc.mensagem},
        )

    @app.get("/health", tags=["Infra"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    api = APIRouter(prefix=API_PREFIX)
    for router in (
        auth_router,
        instituicoes_router,
        eventos_router,
        coordenadores_router,
        atividades_router,
        pessoas_router,
        inscricoes_router,
        presencas_router,
        certificados_router,
        auditoria_router,
        relatorios_router,
    ):
        api.include_router(router)
    app.include_router(api)

    return app


app = create_app()
