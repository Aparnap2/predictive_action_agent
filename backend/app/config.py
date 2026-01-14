"""Configuration and environment validation."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    # App
    app_name: str = "Predictive Action Engine"
    debug: bool = False
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # LLM (Ollama local)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "ingu627/exaone4.0:1.2b"  # Local model

    # Database (for future Prisma integration)
    database_url: str = "postgresql://user:password@localhost:5432/predictive_action"

    # CORS
    frontend_url: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
