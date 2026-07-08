from __future__ import annotations

import math

import httpx

from .config import settings
from .db import locations
from .toollog import log_tool_call


def _distance_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    r = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lng = math.radians(lng2 - lng1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lng / 2) ** 2
    )
    return r * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _geocode_nominatim(query: str) -> dict | None:
    try:
        resp = httpx.get(
            "https://nominatim.openstreetmap.org/search",
            params={"format": "json", "limit": 1, "q": query},
            headers={"User-Agent": "peoples-priorities-mvp/0.2"},
            timeout=2.5,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data:
            return None
        return {"lat": float(data[0]["lat"]), "lng": float(data[0]["lon"])}
    except Exception:
        return None


def resolve_location(
    location_text: str | None = None,
    gps: dict | None = None,
    district_hint: str | None = None,
    state_hint: str | None = None,
    conversation_id: str | None = None,
    agent_type: str = "",
) -> dict:
    """Messy place -> structured geography.

    1) fuzzy name match against known locations
    2) GPS snap to nearest known location within 5km
    3) OSM Nominatim geocode
    """
    result = _resolve_internal(location_text, gps, district_hint, state_hint)
    log_tool_call(
        "resolve_location",
        input_summary=location_text or str(gps or {}),
        output_summary=f"{result['name']} (conf {result['confidence']})",
        conversation_id=conversation_id,
        agent_type=agent_type,
    )
    return result


def match_known_location(text: str | None) -> dict | None:
    """Fuzzy-match free text against known locations only (no GPS, no external
    geocoding). Returns None if there's no confident match - callers must treat
    that as "we have no record of this place" rather than guessing."""
    text = (text or "").strip()
    if not text:
        return None
    tokens = [t for t in _tokenize(text) if len(t) > 2]
    if not tokens:
        return None
    best = None
    best_score = 0
    for loc in locations().find({}):
        name = loc["name"].lower()
        score = sum(len(tk) for tk in tokens if tk in name)
        if score > best_score:
            best_score = score
            best = loc
    if best and best_score >= 4:
        return best
    return None


def _resolve_internal(text: str | None, gps: dict | None, district_hint: str | None, state_hint: str | None) -> dict:
    text = (text or "").strip()

    if text:
        best = match_known_location(text)
        if best:
            tokens = [t for t in _tokenize(text) if len(t) > 2]
            best_score = sum(len(tk) for tk in tokens if tk in best["name"].lower())
            conf = min(0.6 + best_score / 20, 0.92)
            return {
                "location_id": str(best["_id"]),
                "name": best["name"],
                "type": best.get("type", "locality"),
                "district": best.get("district"),
                "state": best.get("state"),
                "lat": best.get("lat"),
                "lng": best.get("lng"),
                "confidence": round(conf, 2),
                "needs_confirmation": conf < 0.8,
            }

    if gps and gps.get("lat") is not None and gps.get("lng") is not None:
        nearest = None
        min_d = float("inf")
        for loc in locations().find({"lat": {"$ne": None}, "lng": {"$ne": None}}):
            d = _distance_km(gps["lat"], gps["lng"], loc["lat"], loc["lng"])
            if d < min_d:
                min_d = d
                nearest = loc
        if nearest and min_d <= 5:
            conf = max(0.5, 0.9 - min_d / 10)
            return {
                "location_id": str(nearest["_id"]),
                "name": nearest["name"],
                "type": nearest.get("type", "locality"),
                "district": nearest.get("district"),
                "state": nearest.get("state"),
                "lat": gps["lat"],
                "lng": gps["lng"],
                "confidence": round(conf, 2),
                "needs_confirmation": conf < 0.8,
            }

    if text:
        geo = _geocode_nominatim(f"{text} {district_hint or ''} {state_hint or ''}")
        if geo:
            return {
                "location_id": None,
                "name": text,
                "type": "locality",
                "district": district_hint,
                "state": state_hint,
                "lat": geo["lat"],
                "lng": geo["lng"],
                "confidence": 0.55,
                "needs_confirmation": True,
            }

    return {
        "location_id": None,
        "name": text or "Unknown",
        "type": "locality",
        "district": district_hint,
        "state": state_hint,
        "lat": gps.get("lat") if gps else None,
        "lng": gps.get("lng") if gps else None,
        "confidence": 0.2,
        "needs_confirmation": True,
    }


def _tokenize(text: str) -> list[str]:
    out: list[str] = []
    cur = ""
    for ch in text.lower():
        if ch.isalnum():
            cur += ch
        else:
            if cur:
                out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return out
