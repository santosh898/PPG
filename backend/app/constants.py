from __future__ import annotations

CATEGORIES = [
    "Water",
    "Roads",
    "Drainage",
    "Streetlights",
    "Pension",
    "Health",
    "Education",
    "Sanitation",
    "Electricity",
    "Other",
]

URGENCY = ["Low", "Medium", "High", "Critical"]

URGENCY_WEIGHT = {
    "Low": 0.25,
    "Medium": 0.5,
    "High": 0.8,
    "Critical": 1.0,
}

CLUSTER_STATUS = [
    "new",
    "verified",
    "forwarded",
    "in_progress",
    "resolved",
    "closed",
]

# Section 24.2 - submissions mentioning these are auto-flagged to staff review.
SENSITIVE_KEYWORDS = [
    "violence",
    "assault",
    "abuse",
    "harassment",
    "rape",
    "molest",
    "suicide",
    "self-harm",
    "self harm",
    "kill",
    "murder",
    "child safety",
    "kidnap",
    "corruption",
    "bribe",
    "criminal",
    "weapon",
    "bomb",
    "threat",
    "defamation",
    "aadhaar",
]

VULNERABLE_GROUP_KEYWORDS = [
    "elderly",
    "old age",
    "senior",
    "pension",
    "children",
    "child",
    "student",
    "school",
    "disabled",
    "disability",
    "handicap",
    "widow",
    "low income",
    "poor",
    "bpl",
]
