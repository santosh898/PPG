# People's Priorities

A conversational **constituency intelligence platform** for elected representatives and their offices. It turns scattered citizen complaints into ranked, evidence-backed development priorities, groups similar issues into clusters, guides citizens to relevant schemes/services/complaint channels, and lets MPs query the constituency knowledge base in natural language.

Built as a single **Next.js (App Router, TypeScript)** app with **MongoDB Atlas + Atlas Vector Search** and an **OpenAI-compatible LLM** (configured for **NVIDIA-hosted DeepSeek** by default) using structured outputs + embeddings.

> This platform does not replace official grievance systems (e.g. CPGRAMS, state PGRS). It is a listening, prioritization, guidance and planning layer.

## Product surfaces

| Route | Who | Purpose |
|---|---|---|
| `/citizen` | Citizens | Conversational issue intake, multilingual, tracking ID + guidance |
| `/staff` | MP office staff | Manual entry, review queue, cluster management, status/publish |
| `/mp/chat` | MP | Natural-language, evidence-backed Q&A over the knowledge base |
| `/mp/dashboard` | MP | Top priorities, category breakdown, hotspots, heatmap, reports |
| `/public/issues` | Public | Anonymized issue clusters + public updates (no personal data) |

## Architecture

- **Structured output (LLM)** handles messy language: language detection, translation, issue extraction, category/urgency, MP query planning, answer grounding. Contracts live in [lib/schemas](lib/schemas/index.ts) as Zod schemas passed to OpenAI structured outputs (`zodResponseFormat`).
- **12 real tools** touch real data/logic in [lib/tools](lib/tools): `resolve_location`, `create_submission`, `find_or_create_issue_cluster`, `get_citizen_guidance`, `search_constituency_knowledge`, `get_priority_issues`, `get_issue_scene`, `get_location_scene`, `get_map_scene`, `generate_report`, `update_issue_status`, `publish_public_update`.
- **Agents** in [lib/agents](lib/agents): the Citizen Intake Agent and MP Intelligence Agent orchestrate structured output + tools, and log every tool call to `ToolCallLog`.
- **Priority scoring** ([lib/scoring/priority.ts](lib/scoring/priority.ts)) is an explainable weighted formula (volume 0.25, urgency 0.25, population 0.20, vulnerable 0.15, trend 0.10, evidence 0.05).
- **Clustering** uses OpenAI embeddings + Atlas `$vectorSearch`, with an automatic in-memory cosine fallback if the index/key is unavailable.

## Prerequisites

- Node.js 18+ (tested on Node 22)
- A free **MongoDB Atlas** cluster (M0 tier supports Vector Search)
- An **NVIDIA API key** (from build.nvidia.com) — or any OpenAI-compatible key (optional; see Fallback mode)

## Setup

```bash
npm install
cp .env.example .env   # then edit values
```

Fill `.env`:

```
MONGODB_URI="mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/peoples_priorities?retryWrites=true&w=majority"
OPENAI_API_KEY="nvapi-..."                              # your NVIDIA API key (optional)
OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"   # NVIDIA OpenAI-compatible endpoint
OPENAI_MODEL="deepseek-ai/deepseek-v4-pro"
OPENAI_EMBEDDING_MODEL="nvidia/nv-embedqa-e5-v5"        # 1024-dim; match the Atlas index
ATLAS_VECTOR_INDEX="cluster_vector_index"
```

The LLM layer targets any OpenAI-compatible API. With DeepSeek on NVIDIA, structured outputs use JSON mode + Zod validation (DeepSeek does not support OpenAI's strict `json_schema`); this is handled automatically in [lib/ai/openai.ts](lib/ai/openai.ts). If the embedding model isn't available, clustering falls back to category+location matching.

### Create the Atlas Vector Search index (one-time)

Semantic clustering uses Atlas Vector Search. In the Atlas UI: **Atlas Search -> Create Search Index -> JSON Editor**, database `peoples_priorities`, collection `issueclusters`, and paste the definition from [docs/atlas-vector-index.json](docs/atlas-vector-index.json). Name it to match `ATLAS_VECTOR_INDEX`. Set `numDimensions` to match your embedding model (1024 for `nvidia/nv-embedqa-e5-v5`, 1536 for OpenAI `text-embedding-3-small`).

If you skip this (or run without an API key), clustering automatically falls back to category + location matching, so the app still works.

## Seed the demo dataset

Seeds one constituency (Visakhapatnam), 7 locations, a curated guidance knowledge base, and ~400 submissions across 10 issue clusters (Section 29 of the spec).

```bash
npm run seed
```

## Run

```bash
npm run dev
# open http://localhost:3000
```

## Demo script (Section 30)

1. **Citizen** (`/citizen`): send "Water has not come in our colony for five days near the old school." The agent structures it, resolves the location, attaches it to the "Water shortage in Madhurwada" cluster, and returns a tracking ID + guidance.
2. **MP chat** (`/mp/chat`): ask "What are the top issues this week?" -> ranked priorities with evidence and confidence badges.
3. Ask "Why is water shortage ranked first?" -> explained from the priority-score breakdown and evidence.
4. Ask "Generate a report for tomorrow's review" -> a weekly priority report.
5. **MP dashboard** (`/mp/dashboard`): top-5 priorities, category chart, hotspots, heatmap, and one-click report.
6. **Staff** (`/staff`): manual entry auto-structures a note; the review queue holds low-confidence/sensitive items; clusters can be status-updated and public updates published.
7. **Public** (`/public/issues`): anonymized clusters and public updates only.

## Fallback mode (no API key)

Without `OPENAI_API_KEY`, the app runs fully with deterministic, keyword-based parsing and category+location clustering. This is ideal for offline demos. With a key, it uses the configured LLM (DeepSeek on NVIDIA by default) via structured outputs and embeddings.

## Privacy & safety (Section 24)

- Public pages expose clusters only — never names, phones, raw text, or home locations.
- Submissions mentioning sensitive keywords are auto-flagged to the staff review queue and never auto-published.
- AI answers show confidence, sources, verification status, and limitations.
- Demographic figures are labelled as public baseline estimates.

## Notes

- `next@14.2.15` is pinned; upgrade to the latest 14.2.x patch to clear the npm security advisory when convenient.
- Data model, tools, APIs and surfaces map 1:1 to Sections 15-24 of the product spec in [idea(1).md](idea(1).md).
