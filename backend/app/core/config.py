from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Powered Breast Cancer Detection and Healthcare Support System"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = Field(
        default="sqlite:///./breast_cancer_detection.db",
        description="Use PostgreSQL in production, for example postgresql://user:pass@db:5432/breast_cancer",
    )
    SECRET_KEY: str = "change-this-secret-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    ALGORITHM: str = "HS256"
    BACKEND_CORS_ORIGINS: str = "http://localhost:8501,http://localhost:3000"
    MODEL_DIR: str = "../ml_models/artifacts"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

