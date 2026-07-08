from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from .ai import get_chat
from .constants import CATEGORIES


class ParsedIssue(BaseModel):
    """Structured fields extracted from a raw citizen/staff note."""

    language: str = Field(description="Detected language of the original text")
    translated_text: str = Field(description="English translation of the issue")
    issue_summary: str = Field(description="One-line neutral summary in English")
    category: str = Field(description=f"One of: {', '.join(CATEGORIES)}")
    secondary_category: str = ""
    urgency: Literal["Low", "Medium", "High", "Critical"] = "Medium"
    duration: Optional[str] = None
    affected_people: Optional[str] = None
    location_text: Optional[str] = None
    sensitive_flags: list[str] = Field(default_factory=list)


_SYSTEM = (
    "You are the issue structuring engine for 'People's Priorities'. Extract "
    "structured fields from a raw citizen/staff note. Translate to English, "
    "classify the category, judge urgency, and flag sensitive content. Do not "
    "invent a location."
)


def parse_issue_text(text: str, language_hint: str | None = None) -> ParsedIssue:
    """Structured extraction via a forced tool call (used by staff manual entry).

    Uses bind_tools (the same reliable tool-calling path the agents use) rather
    than the model's structured-output mode, which is not supported here."""
    model = get_chat().bind_tools([ParsedIssue], tool_choice="required")
    msg = model.invoke(
        [
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": f"Note:\n{text}\n\nLanguage hint: {language_hint or 'unknown'}"},
        ]
    )
    calls = getattr(msg, "tool_calls", None) or []
    if not calls:
        raise RuntimeError("Model did not return structured extraction.")
    return ParsedIssue(**calls[0]["args"])
