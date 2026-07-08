from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from .config import settings

_client: MongoClient | None = None
_db: Database | None = None


def get_db() -> Database:
    global _client, _db
    if _db is None:
        if not settings.mongodb_uri:
            raise RuntimeError("MONGODB_URI is not set.")
        _client = MongoClient(settings.mongodb_uri, tz_aware=True)
        # Use the db in the URI if present, else the configured default.
        default = _client.get_default_database(default=settings.mongodb_db)
        _db = default
    return _db


# Collection accessors (Mongoose default pluralized names).
def users() -> Collection:
    return get_db()["users"]


def conversations() -> Collection:
    return get_db()["conversations"]


def messages() -> Collection:
    return get_db()["messages"]


def locations() -> Collection:
    return get_db()["locations"]


def submissions() -> Collection:
    return get_db()["submissions"]


def issue_clusters() -> Collection:
    return get_db()["issueclusters"]


def evidences() -> Collection:
    return get_db()["evidences"]


def guidance_resources() -> Collection:
    return get_db()["guidanceresources"]


def priority_scores() -> Collection:
    return get_db()["priorityscores"]


def action_updates() -> Collection:
    return get_db()["actionupdates"]


def reports() -> Collection:
    return get_db()["reports"]


def tool_call_logs() -> Collection:
    return get_db()["toolcalllogs"]


def oid(value: Any) -> ObjectId:
    """Coerce a value to an ObjectId."""
    return value if isinstance(value, ObjectId) else ObjectId(str(value))


def now() -> datetime:
    return datetime.now(timezone.utc)


def jsonify(value: Any) -> Any:
    """Recursively make a Mongo document JSON-serializable.

    ObjectId -> str, datetime -> ISO string, and _id -> id kept as str.
    """
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [jsonify(v) for v in value]
    if isinstance(value, dict):
        return {k: jsonify(v) for k, v in value.items()}
    return value
