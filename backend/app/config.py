# [Task]: T010 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Configuration management for Phase 2 backend.
Loads environment variables and provides typed configuration.
"""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = Field(..., alias="DATABASE_URL")

    # JWT Configuration
    jwt_secret: str = Field(..., alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expiration_days: int = Field(default=7, alias="JWT_EXPIRATION_DAYS")

    # CORS Configuration
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:3001,http://127.0.0.1:3000,http://127.0.0.1:3001",
        alias="CORS_ORIGINS"
    )

    # Environment
    environment: str = Field(default="development", alias="ENVIRONMENT")

    # Server Configuration
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=100, alias="RATE_LIMIT_PER_MINUTE")

    # AI Chatbot Configuration (Phase 3)
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    mcp_server_url: str = Field(default="http://localhost:5001", alias="MCP_SERVER_URL")

    @property
    def llm_api_key(self) -> str:
        """Return the best available LLM API key (Groq preferred over Gemini)."""
        return self.groq_api_key or self.gemini_api_key

    @property
    def llm_base_url(self) -> str:
        """Return the base URL for the LLM provider."""
        if self.groq_api_key:
            return "https://api.groq.com/openai/v1"
        return "https://generativelanguage.googleapis.com/v1beta/openai/"

    @property
    def llm_model(self) -> str:
        """Return the model name for the LLM provider."""
        if self.groq_api_key:
            return "llama-3.3-70b-versatile"
        return "gemini-2.0-flash"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS_ORIGINS comma-separated string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
