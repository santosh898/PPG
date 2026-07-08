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

    # ---- Chat / tool-calling: Hugging Face Inference Providers (OpenAI-compatible) ----
    # Pinned to the Groq provider for low, consistent tool-calling latency
    # (~0.5-0.9s/call vs multi-second on the default shared router).
    hf_token: str = ""
    hf_base_url: str = "https://router.huggingface.co/v1"
    chat_model: str = "openai/gpt-oss-120b:groq"

    # ---- Embeddings: Hugging Face hosted Inference API (feature-extraction) ----
    # multilingual-e5-large outputs 1024-dim vectors (matches the Atlas indexes)
    # and covers English/Telugu/Hindi. Requires "query:"/"passage:" prefixes.
    embedding_model: str = "intfloat/multilingual-e5-large"
    embedding_dim: int = 1024

    atlas_vector_index: str = "cluster_vector_index"
    guidance_vector_index: str = "guidance_vector_index"

    default_area_id: str = "CONST_001"
    default_state: str = "Andhra Pradesh"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
