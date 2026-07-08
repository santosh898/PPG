from __future__ import annotations

import math
from functools import lru_cache

from google import genai
from google.genai import types as genai_types
from langchain_google_genai import ChatGoogleGenerativeAI

from .config import settings
from .db import issue_clusters, guidance_resources

# ---------------------------------------------------------------------------
# Chat / tool-calling and embeddings both run through the Google Gemini API,
# using the native langchain-google-genai integration (NOT the OpenAI-
# compatible shim - that endpoint silently ignores reasoning_effort and
# leaves "thinking" on, adding 5-10s of pure overhead per call).
# thinking_budget=0 fully disables reasoning tokens for gemini-2.5-flash-lite,
# which is what makes this model fast enough for a sub-2s agent turn.
# The free tier is quota-based (RPM/RPD) rather than a depleting dollar-
# credit pool, but it is shared capacity and does return transient 503s
# under load - max_retries covers that; it is not a heuristic fallback.
# ---------------------------------------------------------------------------


@lru_cache
def get_chat() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model=settings.chat_model,
        api_key=settings.gemini_api_key,
        temperature=0.2,
        thinking_budget=0,
        max_retries=1,
        timeout=20,
    )


@lru_cache
def _genai_client() -> genai.Client:
    return genai.Client(api_key=settings.gemini_api_key)


def _normalize(vec: list[float]) -> list[float]:
    """gemini-embedding-001 only auto-normalizes the default 3072-dim output;
    at smaller (e.g. 768) dims we must L2-normalize ourselves so cosine
    similarity in Atlas $vectorSearch is comparing directions, not magnitudes."""
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


def _embed(text: str, task_type: str) -> list[float]:
    result = _genai_client().models.embed_content(
        model=settings.embedding_model,
        contents=text[:8000],
        config=genai_types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=settings.embedding_dim,
        ),
    )
    return _normalize(result.embeddings[0].values)


def embed_passage(text: str) -> list[float]:
    """Embed a stored document for later retrieval."""
    return _embed(text, "RETRIEVAL_DOCUMENT")


def embed_query(text: str) -> list[float]:
    """Embed a search query."""
    return _embed(text, "RETRIEVAL_QUERY")


# ---------------------------------------------------------------------------
# Atlas $vectorSearch (no in-memory fallback).
# ---------------------------------------------------------------------------


def search_clusters(
    embedding: list[float],
    category: str | None = None,
    location_id: str | None = None,
    limit: int = 5,
) -> list[dict]:
    stage: dict = {
        "index": settings.atlas_vector_index,
        "path": "embedding",
        "queryVector": embedding,
        "numCandidates": 100,
        "limit": limit,
    }
    filters: dict = {}
    if category:
        filters["category"] = category
    if location_id:
        from bson import ObjectId

        filters["location_ids"] = ObjectId(location_id)
    if filters:
        stage["filter"] = filters
    pipeline = [
        {"$vectorSearch": stage},
        {"$project": {"title": 1, "category": 1, "score": {"$meta": "vectorSearchScore"}}},
    ]
    results = list(issue_clusters().aggregate(pipeline))
    return [
        {"cluster_id": str(r["_id"]), "title": r.get("title", ""), "score": r.get("score", 0.0)}
        for r in results
    ]


def search_guidance_vectors(embedding: list[float], category: str | None = None, limit: int = 6) -> list[dict]:
    stage: dict = {
        "index": settings.guidance_vector_index,
        "path": "embedding",
        "queryVector": embedding,
        "numCandidates": 100,
        "limit": limit,
    }
    if category:
        stage["filter"] = {"category": category}
    pipeline = [
        {"$vectorSearch": stage},
        {
            "$project": {
                "type": 1,
                "name": 1,
                "category": 1,
                "description": 1,
                "url": 1,
                "location_scope": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
    ]
    return list(guidance_resources().aggregate(pipeline))
