import os
from typing import Any, Dict

from app.core.enums import ConfigLLm, ResponseFormat
from app.core.system_prompts.expert_review import expert_review_prompt
from app.infrastructure.utils.decorators.singleton import singleton
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


@singleton
class Settings(BaseSettings):
    APP_NAME: str = "IA Service"
    DEBUG: bool = bool(os.getenv("DEBUG", "True"))
    VERSION: str = "1.0.0"
    # Database settings
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "mongodb")  # mongodb, postgresql
    MONGODB_URL: str = os.getenv(
        "DATABASE_URL",
        "mongodb://admin:password123@mongodb:27017/ai_service?authSource=admin",
    )
    MONGODB_DATABASE: str = os.getenv("MONGODB_DATABASE", "ai_service")
    POSTGRESQL_URL: str = os.getenv("POSTGRESQL_URL", "")
    ALLOW_ORIGINS: str = os.getenv("ALLOW_ORIGINS", "*")

    # API settings
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")

    # Authentication settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-change-this-in-production"
    )
    HASH_ALGORITHM: str = os.getenv("HASH_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Validate required configuration on initialization
        self._validate_required_config()

    def _get_model_name(self) -> str:
        """Get the complete model name from environment variables"""
        provider = os.getenv("AI_PROVIDER", "groq")
        model = os.getenv("AI_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")

        if not provider or not model:
            raise ValueError(
                "AI_PROVIDER and AI_MODEL environment variables are required"
            )

        return f"{provider}{model}"

    def _validate_required_config(self) -> None:
        """Validate that all required configuration is present"""
        required_vars = ["AI_PROVIDER", "AI_MODEL", "OPENAI_API_KEY", "OPENAI_BASE_URL"]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                f"Please set these variables in your .env file or environment."
            )

    @property
    def llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration with proper type conversion"""
        return {
            ConfigLLm.MODEL: self._get_model_name(),
            ConfigLLm.TEMPERATURE: float(os.getenv("TEMPERATURE", "0.7")),
            ConfigLLm.TIMEOUT: int(os.getenv("TIMEOUT", "30")),
            ConfigLLm.TOP_P: 0.9,
            ConfigLLm.MAX_TOKENS: int(os.getenv("MAX_TOKENS", "1000")),
            ConfigLLm.PRESENCE_PENALTY: float(os.getenv("PRESENCE_PENALTY", "0.1")),
            ConfigLLm.FREQUENCY_PENALTY: float(os.getenv("FREQUENCY_PENALTY", "0.1")),
            ConfigLLm.API_KEY: os.getenv("OPENAI_API_KEY"),
            ConfigLLm.OPENAI_BASE_URL: os.getenv(
                "OPENAI_BASE_URL", "https://api.groq.com/openai/v1"
            ),
            ConfigLLm.RESPONSE_FORMAT: ResponseFormat.JSON_OBJECT,
            ConfigLLm.SEED: 42,
            ConfigLLm.STOP_PHRASES: ["##", "END"],
            ConfigLLm.INSTRUCTIONS: os.getenv(
                "EXPERT_REVIEW_PROMPT", expert_review_prompt
            ),
        }
