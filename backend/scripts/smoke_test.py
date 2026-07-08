"""End-to-end smoke test against a running FastAPI server (default :8000).

Usage (from backend/):
    .venv\\Scripts\\python.exe scripts\\smoke_test.py
"""
from __future__ import annotations

import os
import sys

import httpx

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
except Exception:
    pass

BASE = os.environ.get("SMOKE_BASE", "http://127.0.0.1:8000")

passed = 0
failed = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global passed, failed
    mark = "PASS" if cond else "FAIL"
    if cond:
        passed += 1
    else:
        failed += 1
    print(f"[{mark}] {name}{(' - ' + detail) if detail else ''}")


def post(path: str, body: dict) -> dict:
    r = httpx.post(f"{BASE}{path}", json=body, timeout=120)
    r.raise_for_status()
    return r.json()


def get(path: str) -> dict:
    r = httpx.get(f"{BASE}{path}", timeout=120)
    r.raise_for_status()
    return r.json()


def main() -> None:
    print(f"Smoke testing {BASE}\n")

    # 1. Health
    check("health", get("/api/health").get("ok") is True)

    # 2. MP: top issues (tool calling -> get_priorities)
    r = post("/api/mp/chat", {"message": "What are the top issues this week?"})
    print("   MP answer:", (r.get("answer") or "")[:160].replace("\n", " "))
    check("mp top issues answered", bool(r.get("answer")))
    check("mp cited data", len(r.get("data_used", [])) > 0, f"{len(r.get('data_used', []))} sources")
    check("mp priority scene", any(s.get("scene_type") == "priority_scene" for s in r.get("scenes", [])))
    conv = r.get("conversation_id")

    # 3. MP: any road issues (search / priorities + details)
    r = post("/api/mp/chat", {"message": "Any road issues? Why does it matter?", "conversation_id": conv})
    print("   MP answer:", (r.get("answer") or "")[:160].replace("\n", " "))
    check("mp road issues answered", bool(r.get("answer")))
    check("mp road cited data", len(r.get("data_used", [])) > 0)

    # 4. MP: report
    r = post("/api/mp/chat", {"message": "Generate a weekly report for tomorrow's review", "conversation_id": conv})
    check("mp report answered", bool(r.get("answer")))
    check("mp report scene", any(s.get("scene_type") == "report_scene" for s in r.get("scenes", [])))

    # 5. Citizen intake -> file submission
    r = post(
        "/api/citizen/chat",
        {"message": "Water has not come in our colony for five days near the old school in Madhurwada"},
    )
    print("   Citizen reply:", (r.get("reply") or "")[:160].replace("\n", " "))
    sub = r.get("submission")
    check("citizen filed submission", bool(sub and sub.get("tracking_id")), (sub or {}).get("tracking_id", "no tracking id"))
    check("citizen guidance returned", bool(r.get("guidance")))
    tracking = (sub or {}).get("tracking_id")

    # 6. Citizen status lookup
    if tracking:
        r = get(f"/api/submissions/{tracking}")
        check("submission status lookup", r.get("tracking_id") == tracking)

    # 7. Citizen guidance-only question
    r = post("/api/citizen/chat", {"message": "How do I apply for the old age pension scheme?"})
    check("citizen guidance question answered", bool(r.get("reply")))

    # 8. MP dashboard
    r = get("/api/mp/dashboard")
    check("dashboard priorities", len(r.get("priorities", [])) > 0)
    check("dashboard map points", len(r.get("map_points", [])) > 0)
    check("dashboard hotspots", len(r.get("hotspots", [])) > 0)

    # 9. MP priorities REST
    r = get("/api/mp/priorities?limit=5")
    check("priorities REST", len(r.get("priorities", [])) > 0)
    top_cluster = r["priorities"][0]["cluster_id"] if r.get("priorities") else None

    # 10. Issue scene REST
    if top_cluster:
        r = get(f"/api/mp/issues/{top_cluster}/scene")
        check("issue scene REST", r.get("scene_type") == "issue_scene")

    # 11. Map scene REST
    r = get("/api/mp/map-scene")
    check("map scene REST", r.get("scene_type") == "map_scene")

    # 12. Staff: manual entry (LLM structured parse)
    r = post("/api/submissions", {"source": "staff_entry", "original_text": "Street light not working near bus stop in Gajuwaka for a week"})
    check("staff manual entry", bool(r.get("tracking_id")), r.get("cluster_title", ""))
    new_cluster = r.get("cluster_id")

    # 13. Staff: review queue + clusters
    check("review queue", "items" in get("/api/staff/review-queue"))
    r = get("/api/staff/clusters")
    check("clusters list", len(r.get("clusters", [])) > 0)

    # 14. Staff: status update + publish
    if new_cluster:
        r = httpx.patch(f"{BASE}/api/staff/clusters/{new_cluster}/status", json={"status": "verified", "note": "smoke"}, timeout=60).json()
        check("status update", r.get("new_status") == "verified")
        r = post(f"/api/staff/clusters/{new_cluster}/publish", {"message": "We are looking into this issue."})
        check("publish public update", r.get("published") is True)

    # 15. Public issues
    r = get("/api/public/issues")
    check("public issues", len(r.get("issues", [])) > 0)

    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
