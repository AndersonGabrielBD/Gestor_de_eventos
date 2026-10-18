from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base dos models. O schema é criado pelas migrations do Supabase (ADR-01),
    nunca por `Base.metadata.create_all`."""


settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    # O pooler do Supabase (modo transação) não suporta prepared statements em cache.
    connect_args={"statement_cache_size": 0},
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Uma sessão/transação por requisição: commit no sucesso, rollback em erro.
    Assim a ação de impacto e o seu log de auditoria são gravados juntos."""
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
