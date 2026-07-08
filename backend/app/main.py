from __future__ import annotations

from fastapi import Body, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from . import services
from .actions import publish_public_update, update_issue_status
from .agents import run_citizen_agent, run_mp_agent
from .db import jsonify, reports
from .scenes import (
    generate_report,
    get_issue_scene,
    get_location_scene,
    get_map_scene,
    get_priority_issues,
)

app = FastAPI(title="People's Priorities API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


# ------------------------------- Citizen -------------------------------


@app.post("/api/citizen/chat")
def citizen_chat(body: dict = Body(default={})) -> dict:
    return run_citizen_agent(
        message=body.get("message", ""),
        conversation_id=body.get("conversation_id"),
        language_hint=body.get("language_hint"),
    )


# --------------------------------- MP ---------------------------------


@app.post("/api/mp/chat")
def mp_chat(body: dict = Body(default={})) -> dict:
    return run_mp_agent(
        message=body.get("message", ""),
        conversation_id=body.get("conversation_id"),
        area_id=(body.get("filters") or {}).get("area_id"),
    )


@app.get("/api/mp/dashboard")
def mp_dashboard() -> dict:
    return services.mp_dashboard()


@app.get("/api/mp/priorities")
def mp_priorities(
    limit: int = Query(default=10),
    category: str | None = Query(default=None),
) -> dict:
    return get_priority_issues(category=category, limit=limit)


@app.get("/api/mp/map-scene")
def mp_map_scene(
    category: str | None = Query(default=None),
    map_type: str = Query(default="heatmap"),
) -> dict:
    return get_map_scene(category=category, map_type=map_type)


@app.get("/api/mp/issues/{cluster_id}/scene")
def mp_issue_scene(cluster_id: str) -> dict:
    return get_issue_scene(cluster_id) or {"error": "not_found"}


@app.get("/api/mp/locations/{location_id}/scene")
def mp_location_scene(location_id: str) -> dict:
    return get_location_scene(location_id) or {"error": "not_found"}


@app.post("/api/mp/reports")
def mp_reports_create(body: dict = Body(default={})) -> dict:
    return generate_report(area_id=body.get("area_id"))


@app.get("/api/mp/reports")
def mp_reports_list() -> dict:
    rows = list(reports().find({}).sort("created_at", -1).limit(20))
    return {
        "reports": [
            {
                "id": str(r["_id"]),
                "title": r.get("title"),
                "report_type": r.get("report_type"),
                "date_range": r.get("date_range"),
                "sections": r.get("sections", []),
                "created_at": jsonify(r.get("created_at")),
            }
            for r in rows
        ]
    }


# ----------------------------- Submissions -----------------------------


@app.post("/api/submissions")
def submissions_create(body: dict = Body(default={})) -> dict:
    return services.create_submission_api(body)


@app.get("/api/submissions")
def submissions_list() -> dict:
    return services.submissions_list()


@app.get("/api/submissions/{tracking_id}")
def submission_status(tracking_id: str) -> dict:
    return services.submission_status(tracking_id)


# -------------------------------- Staff --------------------------------


@app.get("/api/staff/review-queue")
def staff_review_queue() -> dict:
    return services.staff_review_queue()


@app.get("/api/staff/clusters")
def staff_clusters() -> dict:
    return services.staff_clusters()


@app.patch("/api/staff/clusters/{cluster_id}/status")
def staff_cluster_status(cluster_id: str, body: dict = Body(default={})) -> dict:
    return update_issue_status(
        cluster_id=cluster_id,
        status=body.get("status"),
        note=body.get("note", ""),
        updated_by=body.get("updated_by", "STAFF_001"),
    )


@app.post("/api/staff/clusters/{cluster_id}/publish")
def staff_cluster_publish(cluster_id: str, body: dict = Body(default={})) -> dict:
    return publish_public_update(
        cluster_id=cluster_id,
        message=body.get("message", ""),
        approved_by=body.get("approved_by", "STAFF_001"),
    )


@app.patch("/api/staff/submissions/{submission_id}")
def staff_submission_edit(submission_id: str, body: dict = Body(default={})) -> dict:
    return services.staff_edit_submission(submission_id, body)


# -------------------------------- Public -------------------------------


@app.get("/api/public/issues")
def public_issues(category: str | None = Query(default=None)) -> dict:
    return services.public_issues(category=category)
