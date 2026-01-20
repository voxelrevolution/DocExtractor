# Jan 19 Handoff Notes — DocExtractor

Date: 2026-01-19

## TL;DR (Current State)
- **Core invariant now enforced:** all retrieval/search/comparisons must stay within the **same `client_id` boundary**.
- **Strict ingest contract (Option A) is live:** if the server cannot confidently auto-assign a client and any clients exist, ingestion **must block** and return **HTTP 409** with `detail.error = "client_id_required"`.
- **CLI ingest is compliant:** it handles 409 by listing clients, prompting once, retrying with `client_id`, and reusing the selection.
- **UI has no ingest/upload flow today:** UI calls are primarily **chat** and **export**; documents/review views are mock data.
- **Evidence posture is “audit-grade”:** test outputs and governance audit outputs are captured as files and linked from roadmap/evidence docs.

## How I’ve Been Working (Operating Flow)
This repo is governance-heavy and evidence-driven. The working flow is designed to keep changes **deterministic**, **auditable**, and aligned with the roadmap.

### 1) Anchor on source-of-truth docs before coding
Before implementing anything, re-ground in:
- `README.md` (product scope + operator instructions)
- governance model (`governance/` docs)
- roadmap epic/deliverable/requirement files (`roadmap/`)

This prevents “invented scope” and keeps decisions traceable.

### 2) Treat each change as a contract update
Every feature change is treated as a contract across:
- API payload/schema
- persistence (if DB enabled)
- UI/CLI clients
- tests
- evidence artifacts
- governance/roadmap docs

If one layer changes, follow-through is required to keep the system consistent.

### 3) Prefer strictness over heuristics for boundary safety
For client scoping specifically, strictness is intentional:
- the model can *suggest* a client, but it must be **constrained to known clients**
- when confidence is low and clients exist, the system forces explicit user choice

### 4) Close loops with automated validation + captured evidence
After any meaningful change:
- run backend tests (`pytest`)
- run UI tests (`vitest --run`)
- run governance audit (if governance-related edits)
- store raw outputs under `evidence/E04/test_runs/` (date-stamped)
- link the evidence from the relevant roadmap/evidence docs

No “trust me” validation.

### 5) Minimal, surgical scope
Avoid building “nice to have” UX. Implement only what the roadmap/spec requires. If something doesn’t exist (e.g., UI ingest), don’t invent it; document the limitation and keep the contract accurate.

## Why Job Descriptions Matter (And How They Were Used)
Job descriptions (JDs) are used as a **behavioral and quality contract** for execution.

In practice:
- A JD is loaded to select the correct “operating stance” for a task.
- It drives how decisions are made (e.g., strict contracts, stop-and-ask triggers, evidence requirements).
- It prevents drifting into unsupported scope or style.

Concrete example:
- **AGENT-001 (Orchestration/Architecture)** was used to enforce a contract-first approach: stable API behavior, deterministic fallbacks, and “do not fabricate results.”
- **PM-style JDs** are appropriate when updating roadmaps, trackers, and stakeholder-facing summaries: crisp acceptance criteria, progress clarity, risk surfacing.

If you replace me, continue to:
1) load an appropriate JD for the task,
2) follow its stop/ask rules,
3) write artifacts consistent with the governance model.

## What Was Done (Key Changes Implemented Recently)
### Client boundary & strict ingest workflow
- Added `client_id` (plus optional `project_id`/`batch_id`) scoping across APIs and persistence.
- Implemented `/api/clients` registry endpoints.
- Implemented constrained AI-backed client resolution (allowlisted to known clients).
- Enforced strict Option A:
  - If clients exist AND request lacks `client_id` AND server cannot confidently assign => **409 `client_id_required`** with `client_resolution` payload.

### CLI compatibility
- `scripts/batch_ingest.py` handles 409:
  - fetches `/api/clients`
  - prompts user to select
  - retries ingest with `client_id`
  - caches choice for subsequent documents

### UI wiring (scope)
- UI uses `VITE_DOCEXTRACTOR_CLIENT_ID` to scope:
  - chat requests (`/api/chat`)
  - extraction listing calls in export flow

No UI ingest flow exists today.

### Documentation updates
- Updated `README.md` to document the strict client contract and how to retry on 409.

## Current Validation Evidence (Where to Look)
Evidence files are stored under:
- `evidence/E04/test_runs/`

Most recent reruns:
- `evidence/E04/test_runs/2026-01-19_pytest_full_rerun.txt` (backend)
- `evidence/E04/test_runs/2026-01-19_ui_vitest_run_rerun.txt` (UI)

Earlier (same date) also exists:
- `evidence/E04/test_runs/2026-01-19_pytest_full.txt`
- `evidence/E04/test_runs/2026-01-19_ui_vitest_run.txt`
- `evidence/E04/test_runs/2026-01-19_governance_audit.txt`

Note: repository may not be a git repo (attempting `git status` under `/Reserved/DocExtractor` returned “not a git repository”). Rely on evidence artifacts + file diffs via tooling.

## How to Run the System (Local)
Backend (example with Ollama enabled):
- `DOCEXTRACTOR_OLLAMA_ENABLED=1 DOCEXTRACTOR_OLLAMA_HOST=http://localhost:11434 DOCEXTRACTOR_OLLAMA_MODEL=llama3.1:8b DOCEXTRACTOR_OLLAMA_TIMEOUT_S=20 /Reserved/DocExtractor/.venv/bin/python -m uvicorn src.main:app --host 127.0.0.1 --port 8000`

UI tests:
- `cd ui && npm test -- --run`

Backend tests:
- `cd /Reserved/DocExtractor && /Reserved/DocExtractor/.venv/bin/python -m pytest`

## What’s Next (Recommended Next Tasks)
### 1) FastAPI deprecation cleanup (safe hygiene)
- Tests show deprecation warnings: `@app.on_event("startup")` is deprecated.
- Migrate to FastAPI lifespan handlers in `src/main.py`.
- Capture a new evidence run afterward.

### 2) Confirm all ingestion clients are compatible with 409 contract
- CLI is good.
- If a UI ingest flow is added later, it must implement the same 409 selection + retry behavior.

### 3) Keep governance artifacts aligned
- When adding/closing tasks, update:
  - epic trackers
  - summaries
  - evidence docs linking to raw outputs

## Guardrails / Non-Negotiables
- Never mix corpora across different `client_id` values.
- Do not allow the model to “invent” a client: it must select from known registry only.
- If confidence is low, require explicit user selection (Option A).
- Always produce auditable evidence for test runs and governance checks.

---
End of handoff.
