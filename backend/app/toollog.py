from __future__ import annotations

from .db import tool_call_logs, now


def log_tool_call(
    tool_name: str,
    input_summary: str = "",
    output_summary: str = "",
    conversation_id: str | None = None,
    agent_type: str = "",
) -> None:
    """Audit-log a tool call. Never raises."""
    try:
        tool_call_logs().insert_one(
            {
                "conversation_id": conversation_id,
                "agent_type": agent_type,
                "tool_name": tool_name,
                "input_summary": (input_summary or "")[:500],
                "output_summary": (output_summary or "")[:500],
                "created_at": now(),
            }
        )
    except Exception:
        pass
