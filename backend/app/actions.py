from __future__ import annotations

from .db import action_updates, issue_clusters, now, oid
from .toollog import log_tool_call


def update_issue_status(cluster_id: str, status: str, note: str = "", updated_by: str = "staff") -> dict:
    cluster = issue_clusters().find_one({"_id": oid(cluster_id)})
    if not cluster:
        raise ValueError("Cluster not found")

    update = {"status": status, "updated_at": now()}
    if status == "verified":
        update["verification_status"] = "staff_verified"
    issue_clusters().update_one({"_id": cluster["_id"]}, {"$set": update})

    action_updates().insert_one(
        {
            "cluster_id": cluster["_id"],
            "status": status,
            "note": note or "",
            "visibility": "private",
            "created_by": updated_by or "staff",
            "created_at": now(),
        }
    )
    log_tool_call("update_issue_status", input_summary=f"{cluster_id} -> {status}", output_summary="updated")
    return {"updated": True, "cluster_id": str(cluster["_id"]), "new_status": status}


def publish_public_update(cluster_id: str, message: str, approved_by: str = "staff") -> dict:
    cluster = issue_clusters().find_one({"_id": oid(cluster_id)})
    if not cluster:
        raise ValueError("Cluster not found")

    uid = action_updates().insert_one(
        {
            "cluster_id": cluster["_id"],
            "status": cluster.get("status", "new"),
            "note": message,
            "visibility": "public",
            "created_by": approved_by or "staff",
            "created_at": now(),
        }
    ).inserted_id
    log_tool_call(
        "publish_public_update",
        input_summary=f"{cluster_id}: {message}",
        output_summary=f"published {uid}",
    )
    return {"published": True, "update_id": str(uid), "visible_to_citizens": True}
