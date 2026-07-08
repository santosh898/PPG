from __future__ import annotations

import json
import re
from typing import Optional

from langchain_core.tools import tool

from .clusters import create_submission, find_or_create_cluster
from .constants import CATEGORIES
from .geo import resolve_location as _resolve_location
from .guidance import get_guidance
from .scenes import (
    generate_report as _generate_report,
    get_issue_scene,
    get_priority_issues,
    search_knowledge as _search_knowledge,
)


_OID_RE = re.compile(r"[0-9a-fA-F]{24}")


def _valid_oid(value: str | None) -> str | None:
    """Return value if it looks like a real Mongo ObjectId, else None.

    Models occasionally invent human-readable ids instead of copying the
    exact one from a prior tool result; treat those as absent rather than
    crashing downstream on an invalid ObjectId."""
    if value and _OID_RE.fullmatch(value.strip()):
        return value.strip()
    return None


def normalize_category(value: str | None) -> str | None:
    if not value:
        return None
    v = value.strip().lower()
    for c in CATEGORIES:
        if c.lower() == v:
            return c
    for c in CATEGORIES:
        if c.lower() in v or v in c.lower():
            return c
    return None


# ----------------------------- Citizen tools -----------------------------


@tool
def resolve_location(location_text: str) -> str:
    """Resolve a citizen-described area, ward, village or landmark into a
    structured location with an id. Call this before filing a submission so the
    issue is tied to a place. Returns JSON with location_id (may be null if
    unresolved), name, confidence and needs_confirmation."""
    return json.dumps(_resolve_location(location_text=location_text, state_hint="Andhra Pradesh", agent_type="citizen_agent"))


@tool
def file_submission(
    issue_summary: str,
    category: str,
    location_id: Optional[str] = None,
    location_text: Optional[str] = None,
    urgency: str = "Medium",
    secondary_category: str = "",
    affected_people: str = "",
    duration: str = "",
    original_text: str = "",
) -> str:
    """Record the citizen's issue: creates the submission, groups it with
    similar local issues into a cluster, and returns next-step guidance.

    Only call this once you know the issue and at least an area/location.
    category must be one of: Water, Roads, Drainage, Streetlights, Pension,
    Health, Education, Sanitation, Electricity, Other. Provide location_id from
    resolve_location when available, else location_text. Returns JSON with
    tracking_id, cluster_title, cluster_action, needs_review, guidance."""
    cat = normalize_category(category) or "Other"

    loc_id = _valid_oid(location_id)
    if not loc_id and location_text:
        resolved = _resolve_location(location_text=location_text, state_hint="Andhra Pradesh", agent_type="citizen_agent")
        loc_id = resolved.get("location_id")

    created = create_submission(
        source="citizen_chat",
        original_text=original_text or issue_summary,
        issue_summary=issue_summary,
        category=cat,
        secondary_category=secondary_category,
        urgency=urgency or "Medium",
        location_id=loc_id,
        duration=duration,
        affected_people=affected_people,
        agent_type="citizen_agent",
    )
    cluster = find_or_create_cluster(
        submission_id=created["submission_id"],
        category=cat,
        issue_summary=issue_summary,
        secondary_category=secondary_category,
        location_id=loc_id,
        agent_type="citizen_agent",
    )
    guidance = get_guidance(issue_summary, category=cat, agent_type="citizen_agent")

    return json.dumps(
        {
            "tracking_id": created["tracking_id"],
            "needs_review": created["needs_review"],
            "cluster_title": cluster["cluster_title"],
            "cluster_action": cluster["cluster_action"],
            "guidance": guidance["guidance"],
            "disclaimer": guidance["disclaimer"],
        }
    )


@tool
def search_guidance(query: str, category: Optional[str] = None) -> str:
    """Search the guidance knowledge base (government schemes, complaint portals,
    departments, helplines) for the most relevant next steps for a citizen's
    question. Returns JSON with a list of guidance items."""
    return json.dumps(get_guidance(query, category=normalize_category(category), agent_type="citizen_agent"))


# ------------------------------- MP tools --------------------------------


@tool
def get_priorities(category: Optional[str] = None, limit: int = 5) -> str:
    """Return the ranked top issue clusters for the constituency with submission
    counts, urgency, trend and a score explanation. Use for 'top issues',
    'priorities', 'what matters most'. Returns JSON with a priorities list."""
    return json.dumps(get_priority_issues(category=normalize_category(category), limit=limit, agent_type="mp_agent"))


@tool
def get_issue_details(cluster_id: str) -> str:
    """Get the full evidence packet for ONE issue cluster by its cluster_id:
    metrics, score breakdown, trend, affected groups, recommended actions and
    verification status. Use to explain why an issue matters or ranks where it
    does.

    cluster_id MUST be copied verbatim (the exact 24-character hex string) from
    a cluster_id field already returned by get_priorities or search_knowledge -
    never invent or reformat it. If you don't have one yet, call get_priorities
    or search_knowledge first."""
    if not _valid_oid(cluster_id):
        return json.dumps(
            {
                "error": "invalid_cluster_id",
                "message": (
                    f"'{cluster_id}' is not a valid cluster_id. Call get_priorities or "
                    "search_knowledge and copy the exact cluster_id field from its results."
                ),
            }
        )
    scene = get_issue_scene(cluster_id, agent_type="mp_agent")
    return json.dumps(scene or {"error": "cluster_not_found"})


@tool
def search_knowledge(query: str, category: Optional[str] = None, location_hint: Optional[str] = None) -> str:
    """Semantic search over issue clusters to find issues matching a description
    (e.g. 'pension problems affecting the elderly'). ALWAYS pass location_hint
    when the user names a place (e.g. 'issues in Kommadi') - results are then
    filtered to that place. If the response has location_matched: false, we
    have NO recorded location by that name - tell the user that plainly, do
    NOT present other areas' issues as if they were about the requested place.
    Returns JSON with matching clusters and their ids."""
    return json.dumps(
        _search_knowledge(query, category=normalize_category(category), location_hint=location_hint, agent_type="mp_agent")
    )


@tool
def generate_report() -> str:
    """Generate a weekly constituency priority report (top priorities, hotspots,
    evidence, recommended actions). Use for report/brief/review requests."""
    return json.dumps(_generate_report(agent_type="mp_agent"))


CITIZEN_TOOLS = [resolve_location, file_submission, search_guidance]
MP_TOOLS = [get_priorities, get_issue_details, search_knowledge, generate_report]
