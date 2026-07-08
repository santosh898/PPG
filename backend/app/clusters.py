from __future__ import annotations

from datetime import timedelta

from bson import ObjectId

from .ai import embed_passage, search_clusters
from .constants import SENSITIVE_KEYWORDS, URGENCY, VULNERABLE_GROUP_KEYWORDS
from .db import (
    evidences,
    issue_clusters,
    locations,
    now,
    oid,
    priority_scores,
    submissions,
)
from .scoring import ScoreInputs, compute_priority_score
from .toollog import log_tool_call

SIMILARITY_THRESHOLD = 0.78


def detect_sensitive(text: str) -> list[str]:
    lower = (text or "").lower()
    return [k for k in SENSITIVE_KEYWORDS if k in lower]


def next_tracking_id() -> str:
    year = now().year
    prefix = f"PP-{year}-"
    count = submissions().count_documents({"tracking_id": {"$regex": f"^{prefix}"}})
    return f"{prefix}{str(count + 1).zfill(4)}"


def _highest_urgency(values: list[str]) -> str:
    best = "Low"
    for v in values:
        if v in URGENCY and URGENCY.index(v) > URGENCY.index(best):
            best = v
    return best


def create_submission(
    *,
    source: str,
    original_text: str,
    issue_summary: str,
    category: str,
    translated_text: str = "",
    language: str = "English",
    secondary_category: str = "",
    urgency: str = "Medium",
    location_id: str | None = None,
    duration: str = "",
    affected_people: str = "",
    sensitive_flags: list[str] | None = None,
    evidence_urls: list[str] | None = None,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    tracking_id = next_tracking_id()
    combined = f"{original_text} {translated_text} {issue_summary}"
    flags = sorted(set((sensitive_flags or []) + detect_sensitive(combined)))
    needs_review = len(flags) > 0 or location_id is None
    review_reason = (
        "sensitive_content" if flags else (None if location_id else "low_location_confidence")
    )

    embedding = embed_passage(issue_summary or combined)

    doc = {
        "tracking_id": tracking_id,
        "citizen_id": None,
        "conversation_id": oid(conversation_id) if conversation_id else None,
        "source": source,
        "original_text": original_text,
        "translated_text": translated_text or "",
        "language": language or "English",
        "summary": issue_summary,
        "category": category,
        "secondary_category": secondary_category or "",
        "urgency": urgency or "Medium",
        "status": "submitted",
        "location_id": oid(location_id) if location_id else None,
        "cluster_id": None,
        "affected_people": affected_people or "",
        "duration": duration or "",
        "sensitive_flags": flags,
        "needs_review": needs_review,
        "review_reason": review_reason,
        "embedding": embedding,
        "created_at": now(),
    }
    res = submissions().insert_one(doc)
    submission_id = str(res.inserted_id)

    for url in evidence_urls or []:
        evidences().insert_one(
            {
                "submission_id": res.inserted_id,
                "type": "photo",
                "url": url,
                "visibility": "staff_only",
                "created_at": now(),
            }
        )

    log_tool_call(
        "create_submission",
        input_summary=issue_summary,
        output_summary=f"{tracking_id} ({category})",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return {
        "submission_id": submission_id,
        "tracking_id": tracking_id,
        "status": "submitted",
        "needs_review": needs_review,
    }


def find_or_create_cluster(
    *,
    submission_id: str,
    category: str,
    issue_summary: str,
    secondary_category: str = "",
    location_id: str | None = None,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    submission = submissions().find_one({"_id": oid(submission_id)})
    if not submission:
        raise ValueError("Submission not found")

    matched_id: str | None = None
    similarity = 0.0

    emb = submission.get("embedding")
    if emb:
        matches = search_clusters(emb, category=category, limit=3)
        if matches and matches[0]["score"] >= SIMILARITY_THRESHOLD:
            matched_id = matches[0]["cluster_id"]
            similarity = matches[0]["score"]

    if not matched_id and location_id:
        by_loc = issue_clusters().find_one(
            {
                "category": category,
                "location_ids": oid(location_id),
                "status": {"$nin": ["resolved", "closed"]},
            },
            sort=[("updated_at", -1)],
        )
        if by_loc:
            matched_id = str(by_loc["_id"])
            similarity = 0.7

    if matched_id:
        cluster = issue_clusters().find_one({"_id": oid(matched_id)})
        cluster_action = "attached_to_existing"
    else:
        title = _build_title(category, secondary_category, issue_summary)
        new_doc = {
            "title": title,
            "summary": issue_summary,
            "category": category,
            "secondary_category": secondary_category or "",
            "location_ids": [oid(location_id)] if location_id else [],
            "submission_count": 0,
            "unique_citizen_count": 0,
            "priority_score": 0,
            "urgency": "Medium",
            "verification_status": "unverified",
            "status": "new",
            "affected_groups": [],
            "centroid": {"lat": None, "lng": None},
            "created_at": now(),
            "updated_at": now(),
        }
        cid = issue_clusters().insert_one(new_doc).inserted_id
        cluster = issue_clusters().find_one({"_id": cid})
        cluster_action = "created_new"

    existing_count = cluster.get("submission_count", 0)

    submissions().update_one(
        {"_id": oid(submission_id)},
        {"$set": {"cluster_id": cluster["_id"], "status": "attached_to_cluster"}},
    )

    ensure_cluster_embedding(cluster["_id"])
    recompute_cluster(cluster["_id"])

    log_tool_call(
        "find_or_create_issue_cluster",
        input_summary=issue_summary,
        output_summary=f"{cluster_action} {cluster['title']} (sim {similarity:.2f})",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return {
        "cluster_id": str(cluster["_id"]),
        "cluster_action": cluster_action,
        "cluster_title": cluster["title"],
        "similarity_score": round(similarity, 2),
        "existing_submission_count": existing_count,
    }


def _build_title(category: str, secondary: str, summary: str) -> str:
    base = secondary or summary
    return f"{category} issue" if len(base) > 60 else base


def ensure_cluster_embedding(cluster_id) -> None:
    cluster = issue_clusters().find_one({"_id": oid(cluster_id)})
    if not cluster or cluster.get("embedding"):
        return
    vec = embed_passage(f"{cluster.get('title', '')}. {cluster.get('summary', '')}")
    issue_clusters().update_one({"_id": cluster["_id"]}, {"$set": {"embedding": vec}})


def recompute_cluster(cluster_id) -> dict | None:
    cluster = issue_clusters().find_one({"_id": oid(cluster_id)})
    if not cluster:
        return None

    subs = list(submissions().find({"cluster_id": cluster["_id"]}))
    sub_ids = [s["_id"] for s in subs]
    submission_count = len(subs)
    unique_citizen_count = len(
        {str(s["citizen_id"]) if s.get("citizen_id") else str(s["_id"]) for s in subs}
    )
    urgency = _highest_urgency([s.get("urgency", "Low") for s in subs])

    loc_ids = list({str(s["location_id"]) for s in subs if s.get("location_id")})
    locs = list(locations().find({"_id": {"$in": [oid(i) for i in loc_ids]}}))
    population_estimate = sum(l.get("population_estimate") or 0 for l in locs)
    centroid_pts = [l for l in locs if l.get("lat") is not None and l.get("lng") is not None]
    if centroid_pts:
        centroid = {
            "lat": sum(l["lat"] for l in centroid_pts) / len(centroid_pts),
            "lng": sum(l["lng"] for l in centroid_pts) / len(centroid_pts),
        }
    else:
        centroid = cluster.get("centroid", {"lat": None, "lng": None})

    text = " ".join(
        f"{s.get('summary','')} {s.get('translated_text','')} {s.get('affected_people','')}"
        for s in subs
    ).lower()
    vulnerable_group_hits = sum(1 for k in VULNERABLE_GROUP_KEYWORDS if k in text)
    affected_groups = list(
        dict.fromkeys(
            [(s.get("affected_people") or "").strip() for s in subs if (s.get("affected_people") or "").strip()]
        )
    )[:8]

    half_window = timedelta(days=15)
    cutoff = now() - half_window
    recent_count = sum(1 for s in subs if s["created_at"] >= cutoff)
    previous_count = submission_count - recent_count

    photo_count = evidences().count_documents({"submission_id": {"$in": sub_ids}, "type": "photo"})
    staff_verified = cluster.get("verification_status") == "staff_verified"

    result = compute_priority_score(
        ScoreInputs(
            submission_count=submission_count,
            unique_citizen_count=unique_citizen_count,
            urgency=urgency,
            population_estimate=population_estimate or None,
            affected_location_count=len(loc_ids),
            vulnerable_group_hits=vulnerable_group_hits,
            recent_count=recent_count,
            previous_count=previous_count,
            photo_count=photo_count,
            staff_verified=staff_verified,
        )
    )

    issue_clusters().update_one(
        {"_id": cluster["_id"]},
        {
            "$set": {
                "submission_count": submission_count,
                "unique_citizen_count": unique_citizen_count,
                "urgency": urgency,
                "location_ids": [oid(i) for i in loc_ids],
                "affected_groups": affected_groups,
                "priority_score": result["score"],
                "centroid": centroid,
                "updated_at": now(),
            }
        },
    )

    priority_scores().insert_one(
        {
            "cluster_id": cluster["_id"],
            "score": result["score"],
            "scoring_version": "v1",
            "breakdown": result["breakdown"],
            "explanation": result["explanation"],
            "created_at": now(),
        }
    )
    return issue_clusters().find_one({"_id": cluster["_id"]})
