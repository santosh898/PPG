from __future__ import annotations

from .ai import embed_query, search_guidance_vectors
from .toollog import log_tool_call

DISCLAIMER = (
    "This is informational guidance only. Please verify the final process on the "
    "official source. This platform does not file or track official grievances."
)


def get_guidance(
    query: str,
    category: str | None = None,
    limit: int = 4,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    """Vector search over the guidance knowledge base (schemes, portals,
    departments) for the most relevant next steps for a citizen."""
    vec = embed_query(f"{query} {category or ''}".strip())
    rows = search_guidance_vectors(vec, category=category, limit=max(limit, 6))

    guidance = []
    for r in rows[:limit]:
        conf = round(min(0.6 + float(r.get("score", 0.0)) * 0.35, 0.95), 2)
        guidance.append(
            {
                "type": r.get("type", "guidance"),
                "name": r.get("name", ""),
                "reason": r.get("description") or "Relevant channel for this issue.",
                "url": r.get("url"),
                "confidence": conf,
            }
        )

    log_tool_call(
        "search_guidance",
        input_summary=f"{query} / {category or ''}",
        output_summary=f"{len(guidance)} guidance items",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return {"guidance": guidance, "disclaimer": DISCLAIMER}
