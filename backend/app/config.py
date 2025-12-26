from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database - defaults to SQLite for local dev, use DATABASE_URL env var for PostgreSQL
    DATABASE_URL: str = "sqlite+aiosqlite:///./medbrief.db"

    # JWT
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS - allow all origins in production (Railway provides random URLs)
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:8000"]

    # PubMed
    PUBMED_EMAIL: str = "your_email@example.com"  # Required by NCBI

    class Config:
        env_file = ".env"

    def get_database_url(self) -> str:
        """Convert DATABASE_URL to async format for SQLAlchemy."""
        db_url = self.DATABASE_URL
        # Railway provides postgres:// but SQLAlchemy needs postgresql://
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url


settings = Settings()

