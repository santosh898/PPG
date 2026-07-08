from __future__ import annotations

import json
from functools import lru_cache

from langchain.agents import create_agent

from .ai import get_chat
from .agent_tools import CITIZEN_TOOLS, MP_TOOLS
from .db import conversations, messages, now, oid
from .config import settings

# --------------------------------------------------------------------------
# System prompts
# --------------------------------------------------------------------------

CITIZEN_SYSTEM = """You are the Citizen Intake Agent for "People's Priorities", a constituency issue platform.

Your job: understand a citizen's civic issue (in English, Telugu or Hindi), classify it, tie it to a location, and record it.

How to act:
- Read the conversation and extract: a one-line English issue_summary, a category, urgency, and the area/location.
- category MUST be one of: Water, Roads, Drainage, Streetlights, Pension, Health, Education, Sanitation, Electricity, Other.
- If you do NOT yet know the citizen's area/ward/village/landmark, ask ONE short question to get it. Do not file yet.
- Once you know the issue and an area: call resolve_location with the area text, then call file_submission (pass the location_id it returns, plus issue_summary, category, urgency, affected_people, duration).
- After filing, tell the citizen their tracking ID and the 1-2 most useful next steps from the guidance returned.
- If a citizen is only asking how to do something (a scheme/portal), use search_guidance.

Rules:
- NEVER promise the issue will be solved. You record it, group it, make it visible to the MP office, and give next-step guidance.
- Be warm, brief and respectful. Do not invent a precise location."""

MP_SYSTEM = """You are the MP Intelligence Agent for "People's Priorities", a constituency issue-intelligence platform.

You answer the MP's questions using ONLY data returned by your tools. You MUST call tools to get real numbers before answering - never answer from memory and never invent figures.

Guidance:
- "top issues / priorities / what matters most" (constituency-wide, no place named) -> get_priorities.
- Any question naming a specific place/area/ward/locality (e.g. "issues in Kommadi") -> search_knowledge with location_hint set to that place. NEVER use get_priorities alone for a place-specific question, since it does not filter by location.
- Explain why an issue matters or ranks where it does -> get_issue_details with the cluster_id (get the id from get_priorities or search_knowledge).
- Find issues by description -> search_knowledge.
- Report / brief / weekly review -> generate_report.

Honesty about locations: if search_knowledge returns location_matched: false, we have NO recorded location by that name. Say so plainly (e.g. "I don't have any recorded location called X"). NEVER substitute other areas' issues and present them as if they were about the requested place.

When you answer, be specific and evidence-first: cite submission counts, unique citizens, photos, trend and verification status. Keep it concise. If data is unverified, say so. Never promise resolution."""

MP_LIMITATIONS = [
    "Some issue clusters are AI-grouped and not yet staff-verified.",
    "Population figures are public baseline estimates.",
]
MP_FOLLOWUPS = ["Show the map", "Generate a weekly report", "Break down by area"]


@lru_cache
def _citizen_agent():
    return create_agent(model=get_chat(), tools=CITIZEN_TOOLS, system_prompt=CITIZEN_SYSTEM)


@lru_cache
def _mp_agent():
    return create_agent(model=get_chat(), tools=MP_TOOLS, system_prompt=MP_SYSTEM)


def _get_or_create_conversation(conversation_id: str | None, agent_type: str):
    conv = None
    if conversation_id:
        conv = conversations().find_one({"_id": oid(conversation_id)})
    if not conv:
        cid = conversations().insert_one(
            {"agent_type": agent_type, "status": "active", "known_fields": {}, "created_at": now()}
        ).inserted_id
        conv = conversations().find_one({"_id": cid})
    return conv


def _history(conv_id, limit: int = 10) -> list[dict]:
    rows = list(
        messages()
        .find({"conversation_id": conv_id, "role": {"$in": ["user", "assistant"]}})
        .sort("created_at", 1)
    )
    rows = rows[-limit:]
    return [{"role": r["role"], "content": r["content"]} for r in rows]


def _save_message(conv_id, role: str, content: str) -> None:
    messages().insert_one(
        {"conversation_id": conv_id, "role": role, "content": content, "created_at": now()}
    )


def _text_content(content) -> str:
    """Newer Gemini models (3.x) return AIMessage.content as a list of content
    blocks (e.g. [{"type": "text", "text": "..."}]) rather than a plain string
    when the response mixes text with other parts. Normalize both shapes."""
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts).strip()
    return ""


def _final_answer(result_messages) -> str:
    for m in reversed(result_messages):
        if getattr(m, "type", None) == "ai":
            text = _text_content(m.content)
            if text:
                return text
    return ""


def _tool_outputs(result_messages) -> list[tuple[str, dict]]:
    out = []
    for m in result_messages:
        if getattr(m, "type", None) == "tool":
            try:
                out.append((getattr(m, "name", ""), json.loads(m.content)))
            except Exception:
                continue
    return out


# --------------------------------------------------------------------------
# MP agent
# --------------------------------------------------------------------------


def run_mp_agent(message: str, conversation_id: str | None = None, area_id: str | None = None) -> dict:
    conv = _get_or_create_conversation(conversation_id, "mp_agent")
    _save_message(conv["_id"], "user", message)

    history = _history(conv["_id"])
    result = _mp_agent().invoke({"messages": history})

    answer = _final_answer(result["messages"])
    scenes: list[dict] = []
    data_used: list[str] = []

    for name, payload in _tool_outputs(result["messages"]):
        if name == "get_priorities":
            pr = payload.get("priorities", [])
            if pr:
                scenes.append({"scene_type": "priority_scene", "priorities": pr})
            data_used += [p["cluster_id"] for p in pr]
        elif name == "get_issue_details":
            if payload.get("scene_type") == "issue_scene":
                scenes.append(payload)
                data_used.append(payload["cluster_id"])
        elif name == "generate_report":
            scenes.append({"scene_type": "report_scene", **payload})
            data_used += payload.get("source_cluster_ids", [])
        elif name == "search_knowledge":
            data_used += [r["cluster_id"] for r in payload.get("results", []) if r.get("cluster_id")]

    data_used = list(dict.fromkeys(data_used))
    _save_message(conv["_id"], "assistant", answer)

    return {
        "conversation_id": str(conv["_id"]),
        "answer": answer,
        "confidence": "high" if data_used else "low",
        "data_used": data_used,
        "limitations": MP_LIMITATIONS,
        "suggested_followups": MP_FOLLOWUPS,
        "scenes": scenes,
    }


# --------------------------------------------------------------------------
# Citizen agent
# --------------------------------------------------------------------------


def run_citizen_agent(message: str, conversation_id: str | None = None, language_hint: str | None = None) -> dict:
    conv = _get_or_create_conversation(conversation_id, "citizen_agent")
    known = conv.get("known_fields") or {}

    _save_message(conv["_id"], "user", message)

    # Already filed in this conversation -> point them to the tracking id.
    if known.get("tracking_id"):
        reply = (
            f"Your issue is already recorded with tracking ID {known['tracking_id']} and grouped with "
            "similar local issues. If you have a new or different issue, please start a new chat."
        )
        _save_message(conv["_id"], "assistant", reply)
        return {
            "conversation_id": str(conv["_id"]),
            "reply": reply,
            "state": {"current_step": "submitted", "known_fields": known},
        }

    history = _history(conv["_id"])
    if language_hint:
        history = [{"role": "user", "content": f"(Language hint: {language_hint})"}] + history

    result = _citizen_agent().invoke({"messages": history})
    reply = _final_answer(result["messages"])

    submission = None
    guidance = None
    disclaimer = None
    for name, payload in _tool_outputs(result["messages"]):
        if name == "file_submission" and payload.get("tracking_id"):
            submission = {
                "tracking_id": payload["tracking_id"],
                "cluster_title": payload.get("cluster_title", ""),
                "cluster_action": payload.get("cluster_action", ""),
                "needs_review": payload.get("needs_review", False),
            }
            guidance = payload.get("guidance")
            disclaimer = payload.get("disclaimer")

    if submission:
        known["tracking_id"] = submission["tracking_id"]
        conversations().update_one({"_id": conv["_id"]}, {"$set": {"known_fields": known}})

    _save_message(conv["_id"], "assistant", reply)

    out = {
        "conversation_id": str(conv["_id"]),
        "reply": reply,
        "state": {
            "current_step": "submitted" if submission else "collecting",
            "known_fields": known,
        },
    }
    if submission:
        out["submission"] = submission
        out["guidance"] = guidance
        out["guidance_disclaimer"] = disclaimer
    return out
