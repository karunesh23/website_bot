from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    PROJECT_NAME: str = "ITC Enterprise RAG Chatbot"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str

    OPENAI_API_KEY: str

    LLM_MODEL: str = "gpt-4.1-mini"

    EMBEDDING_MODEL: str = "text-embedding-3-small"

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K: int = 5

    TEMPERATURE: float = 0.2
    MAX_OUTPUT_TOKENS: int = 1024

    KNOWLEDGE_BASE_PATH: str = "app/knowledge_base"

    ELEVENLABS_API_KEY: str | None = None
    ELEVENLABS_VOICE_ID: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()