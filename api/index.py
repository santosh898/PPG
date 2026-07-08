"""Vercel Python serverless entrypoint.

Exposes the existing FastAPI app (defined in ``backend/app/main.py``) as an ASGI
application. Vercel's Python runtime detects the module-level ``app`` object and
serves it. All requests to ``/api/*`` are routed here (see ``next.config.js`` /
``vercel.json``); FastAPI matches on the original ``/api/...`` path.
"""

from __future__ import annotations

import os
import sys

# Ensure the repo root is importable so ``backend`` (a namespace package whose
# ``backend/app`` subpackage has an __init__) resolves both locally and inside
# the bundled Vercel function.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.app.main import app  # noqa: E402  (import after sys.path setup)

# Vercel looks for a module-level ASGI callable named ``app``.
__all__ = ["app"]
