"""One-time migration:

1. Create the Atlas Vector Search indexes (issueclusters + guidanceresources)
   if they do not already exist. On M0 shared clusters this uses the driver's
   search-index API; the JSON definition is also printed so you can create it
   from the Atlas UI if programmatic creation is not permitted.
2. Embed every issue cluster (title + summary) that has no embedding.
3. Embed every guidance resource (name + description + category).

Run from the backend/ directory:
    .venv\\Scripts\\python.exe scripts\\embed_guidance.py
"""
from __future__ import annotations

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo.operations import SearchIndexModel  # noqa: E402

from app.ai import embed_passage  # noqa: E402
from app.config import settings  # noqa: E402
from app.db import guidance_resources, issue_clusters  # noqa: E402

DIM = settings.embedding_dim


def _vector_index_def(filters: list[str]) -> dict:
    fields = [{"type": "vector", "path": "embedding", "numDimensions": DIM, "similarity": "cosine"}]
    fields += [{"type": "filter", "path": f} for f in filters]
    return {"fields": fields}


def ensure_index(col, name: str, filters: list[str]) -> None:
    existing = {i["name"]: i for i in col.list_search_indexes()}
    definition = _vector_index_def(filters)
    if name in existing:
        current_fields = existing[name].get("latestDefinition", {}).get("fields", [])
        current_filters = {f["path"] for f in current_fields if f.get("type") == "filter"}
        if current_filters >= set(filters):
            print(f"[index] '{name}' already exists on {col.name} with required filters")
            return
        print(f"[index] updating '{name}' on {col.name} to add filter fields {set(filters) - current_filters} ...")
        try:
            col.update_search_index(name=name, definition=definition)
            print(f"[index] '{name}' update requested (rebuild takes ~1 min).")
        except Exception as e:
            print(f"[index] could not update programmatically ({type(e).__name__}: {e}).")
            print(json.dumps({"name": name, "type": "vectorSearch", "definition": definition}, indent=2))
        return
    print(f"[index] creating '{name}' on {col.name} ...")
    print(json.dumps({"name": name, "type": "vectorSearch", "definition": definition}, indent=2))
    try:
        col.create_search_index(
            SearchIndexModel(definition=definition, name=name, type="vectorSearch")
        )
        print(f"[index] '{name}' create requested (build takes ~1 min).")
    except Exception as e:  # M0 may reject programmatic creation
        print(f"[index] could not create programmatically ({type(e).__name__}: {e}).")
        print("[index] Create it manually in Atlas UI using the JSON above.")


def embed_clusters() -> None:
    cur = issue_clusters().find({})
    n = 0
    for c in cur:
        text = f"{c.get('title', '')}. {c.get('summary', '')}".strip()
        vec = embed_passage(text)
        issue_clusters().update_one({"_id": c["_id"]}, {"$set": {"embedding": vec}})
        n += 1
        print(f"[cluster] embedded {c.get('title', '')[:50]}")
    print(f"[cluster] embedded {n} clusters")


def embed_guidance() -> None:
    cur = guidance_resources().find({})
    n = 0
    for g in cur:
        text = f"{g.get('name', '')}. {g.get('description', '')}. Category: {g.get('category', '')}".strip()
        vec = embed_passage(text)
        guidance_resources().update_one({"_id": g["_id"]}, {"$set": {"embedding": vec}})
        n += 1
        print(f"[guidance] embedded {g.get('name', '')[:50]}")
    print(f"[guidance] embedded {n} guidance resources")


def main() -> None:
    ensure_index(issue_clusters(), settings.atlas_vector_index, ["category", "status", "location_ids"])
    ensure_index(guidance_resources(), settings.guidance_vector_index, ["category"])
    print("\nEmbedding data ...")
    embed_clusters()
    embed_guidance()
    print("\nWaiting for indexes to finish building (best effort) ...")
    time.sleep(5)
    print("Done.")


if __name__ == "__main__":
    main()
