from __future__ import annotations

from .agent_tools import normalize_category
from .clusters import create_submission, find_or_create_cluster, recompute_cluster
from .config import settings
from .db import (
    action_updates,
    issue_clusters,
    jsonify,
    locations,
    oid,
    submissions,
)
from .geo import resolve_location
from .guidance import get_guidance
from .parse import parse_issue_text
from .scenes import get_map_scene, get_priority_issues


# ------------------------------- MP dashboard -------------------------------


def mp_dashboard() -> dict:
    priorities = get_priority_issues(limit=5)["priorities"]
    map_scene = get_map_scene(map_type="heatmap")

    clusters = list(issue_clusters().find({"status": {"$nin": ["closed"]}}))

    cat_map: dict[str, int] = {}
    for c in clusters:
        cat_map[c["category"]] = cat_map.get(c["category"], 0) + c.get("submission_count", 0)
    category_breakdown = sorted(
        ({"category": k, "submissions": v} for k, v in cat_map.items()),
        key=lambda x: x["submissions"],
        reverse=True,
    )

    loc_subs: dict[str, int] = {}
    for c in clusters:
        for l in c.get("location_ids", []):
            loc_subs[str(l)] = loc_subs.get(str(l), 0) + c.get("submission_count", 0)
    top_loc = sorted(loc_subs.items(), key=lambda x: x[1], reverse=True)[:6]
    locs = list(locations().find({"_id": {"$in": [oid(i) for i, _ in top_loc]}}))
    loc_name = {str(l["_id"]): l["name"] for l in locs}
    hotspots = [{"location": loc_name.get(i, "Unknown"), "submissions": n} for i, n in top_loc]

    rising = [
        {
            "id": str(c["_id"]),
            "title": c["title"],
            "priority_score": c.get("priority_score", 0),
            "submission_count": c.get("submission_count", 0),
        }
        for c in sorted(
            [c for c in clusters if c.get("priority_score", 0) >= 60],
            key=lambda c: c.get("priority_score", 0),
            reverse=True,
        )[:5]
    ]

    unverified_urgent = [
        {
            "id": str(c["_id"]),
            "title": c["title"],
            "urgency": c.get("urgency"),
            "priority_score": c.get("priority_score", 0),
        }
        for c in sorted(
            [
                c
                for c in clusters
                if c.get("verification_status") == "unverified"
                and c.get("urgency") in ("High", "Critical")
            ],
            key=lambda c: c.get("priority_score", 0),
            reverse=True,
        )[:5]
    ]

    return {
        "priorities": priorities,
        "category_breakdown": category_breakdown,
        "hotspots": hotspots,
        "rising": rising,
        "unverified_urgent": unverified_urgent,
        "map_points": map_scene["points"],
    }


# ------------------------------- Staff views -------------------------------


def staff_review_queue() -> dict:
    items = list(submissions().find({"needs_review": True}).sort("created_at", -1).limit(100))
    loc_ids = [s["location_id"] for s in items if s.get("location_id")]
    loc_name = {str(l["_id"]): l["name"] for l in locations().find({"_id": {"$in": loc_ids}})}
    return {
        "items": [
            {
                "type": "submission",
                "id": str(s["_id"]),
                "tracking_id": s.get("tracking_id"),
                "summary": s.get("summary"),
                "category": s.get("category"),
                "urgency": s.get("urgency"),
                "reason": s.get("review_reason") or "review_required",
                "sensitive_flags": s.get("sensitive_flags", []),
                "location": loc_name.get(str(s.get("location_id"))) if s.get("location_id") else None,
                "created_at": jsonify(s.get("created_at")),
            }
            for s in items
        ]
    }


def staff_clusters() -> dict:
    clusters = list(issue_clusters().find({}).sort("priority_score", -1).limit(200))
    loc_ids = list({l for c in clusters for l in c.get("location_ids", [])})
    loc_name = {str(l["_id"]): l["name"] for l in locations().find({"_id": {"$in": loc_ids}})}
    return {
        "clusters": [
            {
                "id": str(c["_id"]),
                "title": c["title"],
                "category": c["category"],
                "submission_count": c.get("submission_count", 0),
                "unique_citizen_count": c.get("unique_citizen_count", 0),
                "priority_score": c.get("priority_score", 0),
                "urgency": c.get("urgency"),
                "status": c.get("status"),
                "verification_status": c.get("verification_status"),
                "locations": [loc_name[str(l)] for l in c.get("location_ids", []) if str(l) in loc_name],
            }
            for c in clusters
        ]
    }


def staff_edit_submission(submission_id: str, body: dict) -> dict:
    s = submissions().find_one({"_id": oid(submission_id)})
    if not s:
        return {"error": "not_found"}
    update: dict = {}
    if body.get("category"):
        update["category"] = body["category"]
    if body.get("urgency"):
        update["urgency"] = body["urgency"]
    if body.get("summary"):
        update["summary"] = body["summary"]
    if body.get("secondary_category"):
        update["secondary_category"] = body["secondary_category"]
    if body.get("location_text"):
        loc = resolve_location(location_text=body["location_text"], state_hint=settings.default_state)
        if loc.get("location_id"):
            update["location_id"] = oid(loc["location_id"])
    if body.get("clear_review"):
        update["needs_review"] = False
        update["review_reason"] = None

    if update:
        submissions().update_one({"_id": s["_id"]}, {"$set": update})
    if s.get("cluster_id"):
        recompute_cluster(s["cluster_id"])
    return {"updated": True, "id": str(s["_id"])}


# --------------------------- Submissions (list/status/create) ---------------


def submissions_list() -> dict:
    subs = list(submissions().find({}).sort("created_at", -1).limit(200))
    loc_ids = [s["location_id"] for s in subs if s.get("location_id")]
    loc_name = {str(l["_id"]): l["name"] for l in locations().find({"_id": {"$in": loc_ids}})}
    return {
        "submissions": [
            {
                "id": str(s["_id"]),
                "tracking_id": s.get("tracking_id"),
                "summary": s.get("summary"),
                "category": s.get("category"),
                "urgency": s.get("urgency"),
                "status": s.get("status"),
                "source": s.get("source"),
                "needs_review": s.get("needs_review"),
                "review_reason": s.get("review_reason"),
                "sensitive_flags": s.get("sensitive_flags", []),
                "location": loc_name.get(str(s.get("location_id"))) if s.get("location_id") else None,
                "cluster_id": str(s["cluster_id"]) if s.get("cluster_id") else None,
                "created_at": jsonify(s.get("created_at")),
            }
            for s in subs
        ]
    }


def submission_status(tracking_id: str) -> dict:
    s = submissions().find_one({"tracking_id": tracking_id})
    if not s:
        return {"error": "not_found"}
    cluster_title = None
    public_updates = []
    if s.get("cluster_id"):
        cluster = issue_clusters().find_one({"_id": s["cluster_id"]})
        cluster_title = cluster["title"] if cluster else None
        updates = action_updates().find(
            {"cluster_id": s["cluster_id"], "visibility": "public"}
        ).sort("created_at", -1)
        public_updates = [{"note": u["note"], "created_at": jsonify(u["created_at"])} for u in updates]
    return {
        "tracking_id": s["tracking_id"],
        "status": s.get("status"),
        "cluster_title": cluster_title,
        "public_updates": public_updates,
    }


def create_submission_api(body: dict) -> dict:
    """POST /api/submissions - staff manual entry or structured payload."""
    source = body.get("source") or "staff_entry"
    payload = body.get("issue_payload") or {}

    category = payload.get("category")
    summary = payload.get("summary") or payload.get("issue_summary")
    secondary = payload.get("secondary_category") or ""
    urgency = payload.get("urgency")
    language = body.get("language") or "English"
    translated = payload.get("translated_text") or body.get("original_text") or ""
    duration = payload.get("duration") or ""
    affected = payload.get("affected_people") or ""
    sensitive = payload.get("sensitive_flags") or []
    location_text = body.get("location_text") or payload.get("location_text")

    if not category or not summary:
        parsed = parse_issue_text(body.get("original_text") or summary or "", body.get("language_hint"))
        category = category or parsed.category
        summary = summary or parsed.issue_summary
        secondary = secondary or parsed.secondary_category
        urgency = urgency or parsed.urgency
        language = parsed.language or language
        translated = translated or parsed.translated_text
        duration = duration or (parsed.duration or "")
        affected = affected or (parsed.affected_people or "")
        sensitive = sensitive or parsed.sensitive_flags
        location_text = location_text or parsed.location_text

    category = normalize_category(category) or "Other"

    location_id = payload.get("location_id")
    if not location_id and location_text:
        loc = resolve_location(location_text=location_text, state_hint=settings.default_state)
        location_id = loc.get("location_id")

    created = create_submission(
        source=source,
        original_text=body.get("original_text") or summary,
        issue_summary=summary,
        category=category,
        translated_text=translated,
        language=language,
        secondary_category=secondary,
        urgency=urgency or "Medium",
        location_id=location_id,
        duration=duration,
        affected_people=affected,
        sensitive_flags=sensitive,
        evidence_urls=body.get("evidence_urls") or [],
    )
    cluster = find_or_create_cluster(
        submission_id=created["submission_id"],
        category=category,
        issue_summary=summary,
        secondary_category=secondary,
        location_id=location_id,
    )
    guidance = get_guidance(summary, category=category)

    return {
        "submission_id": created["submission_id"],
        "tracking_id": created["tracking_id"],
        "cluster_id": cluster["cluster_id"],
        "cluster_title": cluster["cluster_title"],
        "cluster_action": cluster["cluster_action"],
        "needs_review": created["needs_review"],
        "parsed": {
            "category": category,
            "summary": summary,
            "secondary_category": secondary,
            "urgency": urgency or "Medium",
        },
        "guidance": guidance["guidance"],
    }


def public_issues(category: str | None = None) -> dict:
    query: dict = {"status": {"$nin": ["closed"]}, "submission_count": {"$gte": 2}}
    if category:
        query["category"] = category
    clusters = list(issue_clusters().find(query).sort("priority_score", -1).limit(100))
    loc_ids = list({l for c in clusters for l in c.get("location_ids", [])})
    loc_name = {str(l["_id"]): l["name"] for l in locations().find({"_id": {"$in": loc_ids}})}

    cluster_ids = [c["_id"] for c in clusters]
    updates = action_updates().find(
        {"cluster_id": {"$in": cluster_ids}, "visibility": "public"}
    ).sort("created_at", -1)
    by_cluster: dict[str, list] = {}
    for u in updates:
        by_cluster.setdefault(str(u["cluster_id"]), []).append(
            {"note": u["note"], "created_at": jsonify(u["created_at"])}
        )

    return {
        "issues": [
            {
                "id": str(c["_id"]),
                "title": c["title"],
                "category": c["category"],
                "area": ", ".join(
                    loc_name[str(l)] for l in c.get("location_ids", []) if str(l) in loc_name
                ),
                "status": c.get("status"),
                "report_count": c.get("submission_count", 0),
                "public_updates": by_cluster.get(str(c["_id"]), []),
            }
            for c in clusters
        ]
    }
