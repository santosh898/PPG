from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, read from the environment / .env.

    Env var names intentionally match the existing Next.js backend so the same
    credentials work unchanged. The NVIDIA API key lives in OPENAI_API_KEY.
    """

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongodb_uri: str = ""
    # Mongoose connected without a db path, which defaults to "test" on Atlas.
    mongodb_db: str = "test"

    # ---- Chat / tool-calling + embeddings: Google Gemini API ----
    # Free tier is quota-based (RPM/RPD), not a depleting dollar-credit pool.
    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    # Flash-Lite: built for low-latency, high-frequency agentic/tool-calling.
    chat_model: str = "gemini-2.5-flash-lite"

    # ---- Embeddings: gemini-embedding-001 (native google-genai SDK) ----
    # 768 dims via Matryoshka Representation Learning (Google's recommended
    # balance of quality vs. storage). Not auto-normalized at this size - the
    # app L2-normalizes vectors itself (see ai.py) before storing/querying.
    embedding_model: str = "gemini-embedding-001"
    embedding_dim: int = 768

    atlas_vector_index: str = "cluster_vector_index"
    guidance_vector_index: str = "guidance_vector_index"

    default_area_id: str = "CONST_001"
    default_state: str = "Andhra Pradesh"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
