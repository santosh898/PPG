from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from .ai import embed_query, search_clusters
from .config import settings
from .db import (
    action_updates,
    evidences,
    issue_clusters,
    jsonify,
    locations,
    now,
    oid,
    priority_scores,
    reports,
    submissions,
)
from .toollog import log_tool_call


def _trend_label(recency: float | None) -> str:
    if recency is None:
        return "stable"
    if recency >= 6:
        return "increasing"
    if recency <= 4:
        return "decreasing"
    return "stable"


def _default_range_days(days: int = 7) -> tuple[datetime, datetime]:
    to = now()
    return to - timedelta(days=days), to


def get_priority_issues(
    category: str | None = None,
    limit: int = 10,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    frm, to = _default_range_days(7)
    query: dict = {"updated_at": {"$gte": frm, "$lte": to}, "status": {"$nin": ["closed"]}}
    if category:
        query["category"] = category

    clusters = list(issue_clusters().find(query).sort("priority_score", -1).limit(limit))
    if not clusters:
        fb: dict = {"status": {"$nin": ["closed"]}}
        if category:
            fb["category"] = category
        clusters = list(issue_clusters().find(fb).sort("priority_score", -1).limit(limit))

    priorities = []
    for rank, c in enumerate(clusters, start=1):
        loc = None
        if c.get("location_ids"):
            loc = locations().find_one({"_id": c["location_ids"][0]})
        latest = priority_scores().find_one({"cluster_id": c["_id"]}, sort=[("created_at", -1)])
        priorities.append(
            {
                "rank": rank,
                "cluster_id": str(c["_id"]),
                "title": c.get("title", ""),
                "category": c.get("category", ""),
                "location": loc["name"] if loc else "Constituency",
                "submission_count": c.get("submission_count", 0),
                "unique_citizen_count": c.get("unique_citizen_count", 0),
                "urgency": c.get("urgency", "Medium"),
                "priority_score": c.get("priority_score", 0),
                "trend": _trend_label((latest or {}).get("breakdown", {}).get("recency_trend")),
                "reason": (latest or {}).get("explanation", ""),
            }
        )

    log_tool_call(
        "get_priority_issues",
        input_summary=f"cat={category or 'all'} limit={limit}",
        output_summary=f"{len(priorities)} priorities",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return {"priorities": priorities}


def _recommend(category: str, verification: str) -> list[str]:
    actions: list[str] = []
    if verification == "unverified":
        actions.append("Run field verification")
    actions.append("Forward to relevant local department")
    if category in ("Water", "Drainage", "Health", "Sanitation"):
        actions.append("Send public health/safety advisory")
    if category == "Pension":
        actions.append("Run a pension support desk / helpdesk")
    return actions


def _change_percent(explanation: str | None) -> int | None:
    if not explanation:
        return None
    m = re.search(r"(-?\d+)%", explanation)
    return int(m.group(1)) if m else None


def get_issue_scene(
    cluster_id: str,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict | None:
    c = issue_clusters().find_one({"_id": oid(cluster_id)})
    if not c:
        return None
    loc = locations().find_one({"_id": c["location_ids"][0]}) if c.get("location_ids") else None
    sub_ids = [s["_id"] for s in submissions().find({"cluster_id": c["_id"]}, {"_id": 1})]
    photos = evidences().count_documents({"submission_id": {"$in": sub_ids}, "type": "photo"})
    latest = priority_scores().find_one({"cluster_id": c["_id"]}, sort=[("created_at", -1)])
    updates = list(action_updates().find({"cluster_id": c["_id"]}).sort("created_at", -1).limit(5))
    recency = (latest or {}).get("breakdown", {}).get("recency_trend", 5)

    scene = {
        "scene_type": "issue_scene",
        "cluster_id": str(c["_id"]),
        "title": c.get("title", ""),
        "summary": c.get("summary", ""),
        "category": c.get("category", ""),
        "location": {"name": loc["name"] if loc else "Constituency", "district": (loc or {}).get("district")},
        "metrics": {
            "submissions": c.get("submission_count", 0),
            "unique_citizens": c.get("unique_citizen_count", 0),
            "photos": photos,
            "priority_score": c.get("priority_score", 0),
        },
        "trend": {
            "direction": _trend_label(recency),
            "change_percent": _change_percent((latest or {}).get("explanation")),
        },
        "score_breakdown": (latest or {}).get("breakdown"),
        "affected_groups": c.get("affected_groups", []),
        "recommended_actions": _recommend(c.get("category", ""), c.get("verification_status", "unverified")),
        "verification": {
            "status": c.get("verification_status", "unverified"),
            "staff_review_required": c.get("verification_status") == "unverified",
        },
        "status": c.get("status", "new"),
        "action_updates": [
            {
                "status": u.get("status"),
                "note": u.get("note"),
                "created_at": jsonify(u.get("created_at")),
                "visibility": u.get("visibility"),
            }
            for u in updates
        ],
        "explanation": (latest or {}).get("explanation", ""),
    }
    log_tool_call(
        "get_issue_scene",
        input_summary=cluster_id,
        output_summary=f"{scene['title']} score {scene['metrics']['priority_score']}",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return scene


def get_location_scene(
    location_id: str,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict | None:
    loc = locations().find_one({"_id": oid(location_id)})
    if not loc:
        return None
    clusters = list(
        issue_clusters()
        .find({"location_ids": loc["_id"], "status": {"$nin": ["closed"]}})
        .sort("priority_score", -1)
        .limit(8)
    )
    scene = {
        "scene_type": "location_scene",
        "location": {
            "id": str(loc["_id"]),
            "name": loc["name"],
            "type": loc.get("type"),
            "district": loc.get("district"),
        },
        "top_issues": [
            {
                "cluster_id": str(c["_id"]),
                "title": c.get("title", ""),
                "category": c.get("category", ""),
                "submissions": c.get("submission_count", 0),
                "priority_score": c.get("priority_score", 0),
            }
            for c in clusters
        ],
        "demographic_context": {
            "population_estimate": loc.get("population_estimate"),
            "households": loc.get("households"),
            "source": "open public dataset",
            "limitations": "Baseline estimate from public data; not a real-time population figure.",
        },
    }
    log_tool_call(
        "get_location_scene",
        input_summary=location_id,
        output_summary=f"{loc['name']}: {len(clusters)} issues",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return scene


def get_map_scene(
    category: str | None = None,
    map_type: str = "heatmap",
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    query: dict = {"status": {"$nin": ["closed"]}}
    if category:
        query["category"] = category
    clusters = list(issue_clusters().find(query))
    points = []
    for c in clusters:
        lat = (c.get("centroid") or {}).get("lat")
        lng = (c.get("centroid") or {}).get("lng")
        if (lat is None or lng is None) and c.get("location_ids"):
            loc = locations().find_one({"_id": c["location_ids"][0]})
            lat = (loc or {}).get("lat")
            lng = (loc or {}).get("lng")
        if lat is None or lng is None:
            continue
        points.append(
            {
                "lat": lat,
                "lng": lng,
                "weight": c.get("submission_count", 0),
                "label": c.get("title", ""),
                "cluster_id": str(c["_id"]),
                "category": c.get("category", ""),
                "priority_score": c.get("priority_score", 0),
            }
        )
    log_tool_call(
        "get_map_scene",
        input_summary=f"cat={category or 'all'}",
        output_summary=f"{len(points)} points",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return {"scene_type": "map_scene", "map_type": map_type, "points": points}


def search_knowledge(
    query: str,
    category: str | None = None,
    location_hint: str | None = None,
    limit: int = 10,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    """Semantic search over issue clusters. If location_hint is given, this
    resolves it against known locations FIRST and filters results to that
    location - it never silently returns unrelated clusters framed as if they
    were about a place we have no record of."""
    from .geo import match_known_location

    location_matched = None
    if location_hint:
        matched_loc = match_known_location(location_hint)
        if not matched_loc:
            log_tool_call(
                "search_constituency_knowledge",
                input_summary=query,
                output_summary=f"no location match for '{location_hint}'",
                conversation_id=conversation_id,
                agent_type=agent_type,
            )
            return {
                "location_hint": location_hint,
                "location_matched": False,
                "results": [],
                "note": (
                    f"No known location matches '{location_hint}'. Do not present other "
                    "areas' issues as if they relate to this place - tell the user we have "
                    "no recorded location by that name."
                ),
            }
        location_matched = matched_loc

    results = []
    seen: set[str] = set()
    vec = embed_query(query)
    matches = search_clusters(
        vec,
        category=category,
        location_id=str(location_matched["_id"]) if location_matched else None,
        limit=limit,
    )
    for m in matches:
        cid = m["cluster_id"]
        if cid in seen:
            continue
        c = issue_clusters().find_one({"_id": oid(cid)})
        if not c:
            continue
        loc = locations().find_one({"_id": c["location_ids"][0]}) if c.get("location_ids") else None
        seen.add(cid)
        results.append(
            {
                "type": "issue_cluster",
                "cluster_id": cid,
                "title": c.get("title", ""),
                "submission_count": c.get("submission_count", 0),
                "priority_score": c.get("priority_score", 0),
                "location": loc["name"] if loc else None,
                "category": c.get("category", ""),
            }
        )

    output: dict = {"results": results[:limit]}
    if location_hint:
        output["location_hint"] = location_hint
        output["location_matched"] = True
        output["matched_location_name"] = location_matched["name"]
        if not results:
            output["note"] = f"No recorded issues in {location_matched['name']} yet."

    log_tool_call(
        "search_constituency_knowledge",
        input_summary=query,
        output_summary=f"{len(results)} results",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return output


def _dedupe_by(items: list[dict], key) -> list[dict]:
    seen: set = set()
    out = []
    for x in items:
        k = key(x)
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def generate_report(
    area_id: str | None = None,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    frm, to = _default_range_days(7)
    priorities = get_priority_issues(limit=5)["priorities"]

    top_scenes = []
    for p in priorities[:3]:
        s = get_issue_scene(p["cluster_id"])
        if s:
            top_scenes.append(s)

    top_text = (
        "\n".join(
            f"{p['rank']}. {p['title']} - {p['submission_count']} submissions, "
            f"{p['urgency']} urgency, {p['trend']} trend (score {p['priority_score']})."
            for p in priorities
        )
        or "No priority issues recorded in this period."
    )
    hotspots = "\n".join(
        f"{p['location']}: {p['title']} ({p['submission_count']} reports)"
        for p in _dedupe_by(priorities, lambda p: p["location"])
    )
    evidence = "\n".join(
        f"{s['title']}: {s['metrics']['submissions']} submissions, "
        f"{s['metrics']['unique_citizens']} unique citizens, {s['metrics']['photos']} photos. "
        f"Verification: {s['verification']['status']}."
        for s in top_scenes
    )
    actions = "\n".join(
        f"{s['title']}: {a}" for s in top_scenes for a in s["recommended_actions"]
    )
    action_lines = "\n".join(actions.split("\n")[:6])

    sections = [
        {"heading": "Top Priorities", "content": top_text},
        {"heading": "Location Hotspots", "content": hotspots or "No hotspots identified."},
        {"heading": "Evidence Summary", "content": evidence or "No evidence attached yet."},
        {"heading": "Recommended Actions", "content": action_lines or "No actions recommended yet."},
        {
            "heading": "Source Issue Clusters",
            "content": "\n".join(f"{p['cluster_id']} - {p['title']}" for p in priorities),
        },
        {
            "heading": "Data Limitations",
            "content": (
                "Some clusters are AI-grouped and not yet staff-verified. Population figures are "
                "public baseline estimates. Verify before public communication."
            ),
        },
    ]

    date_range = {"from": frm.isoformat(), "to": to.isoformat()}
    doc = {
        "title": "Weekly Constituency Priority Report",
        "report_type": "weekly_priority_report",
        "area_id": area_id or settings.default_area_id,
        "date_range": date_range,
        "sections": sections,
        "source_cluster_ids": [oid(p["cluster_id"]) for p in priorities],
        "format": "markdown",
        "created_at": now(),
    }
    rid = reports().insert_one(doc).inserted_id

    log_tool_call(
        "generate_report",
        input_summary="weekly_priority_report",
        output_summary=f"{rid} ({len(sections)} sections)",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return {
        "report_id": str(rid),
        "title": doc["title"],
        "date_range": date_range,
        "sections": sections,
        "source_cluster_ids": [p["cluster_id"] for p in priorities],
    }
