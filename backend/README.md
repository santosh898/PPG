# People's Priorities — Python Backend

FastAPI + LangGraph (LangChain v1 `create_agent`) backend. It replaces the old
TypeScript API routes. The Next.js frontend proxies `/api/*` to this service via
a rewrite in `next.config.js`.

- **LLM / tool-calling:** Hugging Face Inference Providers (OpenAI-compatible
  router at `https://router.huggingface.co/v1`), model `deepseek-ai/DeepSeek-V3-0324`
- **Embeddings:** local `sentence-transformers` (`intfloat/multilingual-e5-large`,
  1024-dim) — no API/token required, runs on CPU
- **Vector search:** MongoDB Atlas `$vectorSearch` (`cluster_vector_index`,
  `guidance_vector_index`) — no in-memory fallback
- **DB:** existing Atlas cluster, database `test`

Config is read from the repo-root `.env` (via `../.env`): `MONGODB_URI`,
`HF_TOKEN` (from https://huggingface.co/settings/tokens, needs "Inference
Providers" permission), `HF_BASE_URL`, `CHAT_MODEL`, `EMBEDDING_MODEL`,
`EMBEDDING_DIM`.

> Note: NVIDIA's `deepseek-v4-flash` isn't available on HF (DeepSeek only
> publishes the raw V4 weights there; no provider serves it). `DeepSeek-V3-0324`
> is the closest tool-calling model actually served by HF Inference Providers.

## Setup

```powershell
cd backend
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## One-time migration (indexes + embeddings)

Creates the two Atlas vector indexes (or prints the JSON to create them in the
Atlas UI) and embeds all issue clusters + guidance resources:

```powershell
.\.venv\Scripts\python.exe scripts\embed_guidance.py
```

## Run

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then run the Next.js frontend from the repo root (`npm run dev`); it proxies
`/api/*` to `http://127.0.0.1:8000`. Override the target with `BACKEND_URL`.

## Smoke test (server must be running)

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test.py
```

## Layout

| Path | Purpose |
|------|---------|
| `app/config.py` | env settings |
| `app/db.py` | Mongo client + collection accessors |
| `app/ai.py` | `ChatNVIDIA` (with transient-error retry), embeddings, `$vectorSearch` |
| `app/scoring.py` | priority score v1 |
| `app/clusters.py` | submission + cluster create / recompute |
| `app/geo.py` | location resolution (name / GPS / Nominatim) |
| `app/guidance.py` | guidance KB vector search |
| `app/scenes.py` | priorities, issue/location/map scenes, report, knowledge search |
| `app/actions.py` | staff status update / public update |
| `app/parse.py` | structured extraction for staff manual entry (forced tool call) |
| `app/agent_tools.py` | LangChain tools for both agents |
| `app/agents.py` | citizen + MP `create_agent` agents |
| `app/services.py` | dashboard / review / clusters / submissions / public |
| `app/main.py` | FastAPI app + all 16 routes |
