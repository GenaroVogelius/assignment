from enum import Enum, StrEnum


class Models(StrEnum):
    LLAMA_4_SCOUT_17B_16E_INSTRUCT = "meta-llama/llama-4-scout-17b-16e-instruct"


class ConfigLLm(StrEnum):
    MODEL = "model"
    TEMPERATURE = "temperature"
    TOP_P = "top_p"
    MAX_TOKENS = "max_tokens"
    PRESENCE_PENALTY = "presence_penalty"
    FREQUENCY_PENALTY = "frequency_penalty"
    API_KEY = "api_key"
    OPENAI_BASE_URL = "base_url"
    RESPONSE_FORMAT = "response_format"
    SEED = "seed"
    STOP_PHRASES = "stop_phrases"
    TIMEOUT = "timeout"
    INSTRUCTIONS = "instructions"


class ResponseFormat:
    """Response format constants for LLM configuration"""

    TEXT = {"type": "text"}
    JSON_OBJECT = {"type": "json_object"}


class DatabaseType(Enum):
    """Supported database types"""

    MONGODB = "mongodb"
    POSTGRESQL = "postgresql"