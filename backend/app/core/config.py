from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ambiente: str = "dev"
    database_url: str = "postgresql+asyncpg://postgres:postgres@127.0.0.1:54322/postgres"

    supabase_url: str = "http://127.0.0.1:54321"
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""

    cors_origins: list[str] = ["http://localhost:5173"]
    url_publica_validacao: str = "http://localhost:5173/validar"

    chave_cifragem_dados: str = ""
    chave_hmac_dados: str = ""

    @property
    def jwks_url(self) -> str:
        return f"{self.supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"


@lru_cache
def get_settings() -> Settings:
    return Settings()
