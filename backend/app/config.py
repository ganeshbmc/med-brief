from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./medbrief.db"

    # JWT
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]  # Vite default

    # PubMed
    PUBMED_EMAIL: str = "your_email@example.com"  # Required by NCBI

    class Config:
        env_file = ".env"


settings = Settings()
