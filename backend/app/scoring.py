from __future__ import annotations

from dataclasses import dataclass

from .constants import URGENCY_WEIGHT

WEIGHTS = {
    "submission_volume": 0.25,
    "urgency": 0.25,
    "affected_population": 0.20,
    "vulnerable_group_impact": 0.15,
    "recency_trend": 0.10,
    "evidence_quality": 0.05,
}

_LABELS = {
    "submission_volume": "high complaint volume",
    "urgency": "affects an essential/urgent service",
    "affected_population": "impacts a large or dense area",
    "vulnerable_group_impact": "affects vulnerable groups",
    "evidence_quality": "has supporting evidence",
}


def _clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


def _round1(n: float) -> float:
    return round(n * 10) / 10


@dataclass
class ScoreInputs:
    submission_count: int
    unique_citizen_count: int
    urgency: str
    population_estimate: int | None
    affected_location_count: int
    vulnerable_group_hits: int
    recent_count: int
    previous_count: int
    photo_count: int
    staff_verified: bool


def compute_priority_score(i: ScoreInputs) -> dict:
    """Port of the Section 19 priority score (v1). Weighted contributions sum
    to the final 0..100 score."""
    volume_raw = i.unique_citizen_count or i.submission_count
    volume = _clamp((volume_raw / 60) * 100, 0, 100)

    urgency = (URGENCY_WEIGHT.get(i.urgency, 0.5)) * 100

    pop_component = (
        _clamp((i.population_estimate / 20000) * 100, 0, 100)
        if i.population_estimate
        else 40
    )
    spread_component = _clamp(i.affected_location_count * 15, 0, 100)
    affected_population = _clamp(pop_component * 0.6 + spread_component * 0.4, 0, 100)

    vulnerable = _clamp(i.vulnerable_group_hits * 25, 0, 100)

    trend = 50.0
    if i.previous_count > 0:
        change = (i.recent_count - i.previous_count) / i.previous_count
        trend = _clamp(50 + change * 100, 0, 100)
    elif i.recent_count > 0:
        trend = 80.0

    evidence = _clamp(
        _clamp(i.photo_count * 8, 0, 60)
        + (25 if i.staff_verified else 0)
        + _clamp(i.unique_citizen_count * 2, 0, 15),
        0,
        100,
    )

    breakdown = {
        "submission_volume": _round1(volume * WEIGHTS["submission_volume"]),
        "urgency": _round1(urgency * WEIGHTS["urgency"]),
        "affected_population": _round1(affected_population * WEIGHTS["affected_population"]),
        "vulnerable_group_impact": _round1(vulnerable * WEIGHTS["vulnerable_group_impact"]),
        "recency_trend": _round1(trend * WEIGHTS["recency_trend"]),
        "evidence_quality": _round1(evidence * WEIGHTS["evidence_quality"]),
    }

    score = _round1(sum(breakdown.values()))
    return {"score": score, "breakdown": breakdown, "explanation": _explain(i, breakdown, trend)}


def _explain(i: ScoreInputs, b: dict, trend: float) -> str:
    labels = dict(_LABELS)
    labels["recency_trend"] = "is increasing recently" if trend > 55 else "recent activity"
    ranked = sorted(b.items(), key=lambda kv: kv[1], reverse=True)
    parts = [labels[k] for k, v in ranked[:3] if v > 0]
    base = f"Ranked by {', '.join(parts)}."
    stats = f" Based on {i.submission_count} submissions from {i.unique_citizen_count} unique citizens"
    if i.previous_count > 0:
        pct = round(((i.recent_count - i.previous_count) / i.previous_count) * 100)
        growth = f", {pct}% change vs previous period."
    else:
        growth = "."
    return base + stats + growth
