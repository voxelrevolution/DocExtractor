# Local Document Extraction Copilot

## Purpose
A privacy-first, local-first desktop application that ingests financial documents (PDF/XLS/XLSX/DOC/DOCX), extracts structured data (especially invoices), and provides a Copilot-style interface for querying and working with the extracted corpus locally on GPU.

## Non-Negotiables
- **Private-by-Design:** No cloud inference by default; operate fully offline
- **GPU-First Inference:** AI inference workloads must utilize GPU
- **Evidence-Backed Extraction:** Every extracted field must have source evidence pointers
- **Governance-First Delivery:** Strict Roadmap → Epic → Deliverable → Requirement → Task → JD-assigned workflow
- **Modular Codebase:** Code organization and architecture prioritizes modularity, reusability, and clear separation of concerns across all layers (API, data, observability, LLM, database)

## How to Navigate This Project

**For the AI (me):**  
When context resets, read in this order:
1. This README (you're reading it)
2. [Governance Essentials](governance/GOVERNANCE_SIMPLIFIED.md) (5 min)
3. [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) (where are we?)
4. Task specification file (what am I doing?)

**For you (UAT/Decision-Maker):**  
- **Current status:** [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md)
- **How work is organized:** [Governance Essentials](governance/GOVERNANCE_SIMPLIFIED.md)
- **Detailed epic status:** [Evidence/Epic Trackers](#current-project-status)

### Repository Structure

```text
/Reserved/DocExtractor/
│
├── README.md                           ← START HERE (you are here)
├── PROJECT_STATUS_DASHBOARD.md         ← Current status (check this first)
│
├── governance/
│   ├── GOVERNANCE_SIMPLIFIED.md        ← How we organize work (5 min read)
│   ├── DECISION_LOG.md                 ← Why decisions were made
│   └── (other governance reference docs)
│
├── roadmap/
│   └── R01_LocalDocExtractionPlatform/
│       ├── roadmap.md                  ← Master plan (5 epics)
│       └── epics/
│           ├── E01_CoreFoundation/
│           │   ├── epic.md             ← What epic delivers
│           │   ├── deliverables/       ← D0X.Y_Name/ (what's being built)
│           │   │   └── D01.1_Name/
│           │   │       ├── deliverable.md
│           │   │       └── requirements/  ← R0X.Y_Name/ (acceptance criteria)
│           │   │           └── R01.1.1_Name/
│           │   │               ├── requirement.md
│           │   │               └── tasks/  ← T0X.Y.Z_JD-NNN_Name.md
│           │   └── summaries/          ← Epic-level docs (DoD, executive summary)
│           │
│           ├── E02_IngestionLibrary/        ← Same structure
│           ├── E03_InvoiceExtractionPipeline/ ← Same structure
│           ├── E04_CopilotInterface/        ← Same structure
│           └── E05_ProductionReadiness/     ← Same structure
│
├── evidence/                            ← DEPRECATED: Evidence now lives co-located with requirements
│
├── roadmap/
│   └── R01_LocalDocExtractionPlatform/
│       ├── epic.md
│       └── epics/
│           └── E0X_EpicName/
│               ├── deliverables/
│               │   └── D0X.Y_Name/
│               │       ├── requirements/
│               │       │   └── R0X.Y_Name/
│               │       │       ├── requirement.md
│               │       │       ├── tasks/
│               │       │       │   └── T0X.Y.Z_JD-NNN_*.md
│               │       │       └── evidence/         ← ✅ Task artifacts here (co-located)
│               │       │           └── T0X.Y.Z_JD-NNN_Report.md
│               │       └── ...
│               └── E0X_EXECUTION_TRACKER.md         ← Epic progress tracking
│
├── src/                                 ← Application code
├── tests/                               ← Test suite
├── docs/                                ← Developer setup, architecture docs
├── scripts/                             ← Setup & utility scripts
│
└── docker-compose.yml, requirements.txt, etc.
```

**Key points:**
- Epic → Deliverable → Requirement → Task (follows this hierarchy)
- Task files named `T0X.Y.Z_JD-NNN_[Name].md` (JD-ID always included)
- **Evidence stored co-located:** `/roadmap/.../requirements/R0X.Y/evidence/` (not root-level `/evidence/`)
- Execution tracked in `PROJECT_STATUS_DASHBOARD.md` (master tracking) and `E0X_EXECUTION_TRACKER.md` (detailed)

## How Work Gets Done

**Roadmap** (master plan) → **Epic** (major outcome) → **Deliverable** (component) → **Requirement** (acceptance criteria) → **Task** (executable unit) → **JD** (who does it) → **Evidence** (proof it's done)

**Every task file** includes its JD-ID in the filename: `T02.1.1_JD-DATA027_ImportDesign.md`

**Every requirement** has explicit acceptance criteria. Task is complete when all criteria are met + evidence is collected.

**Every deliverable** has a Definition of Done (8 quality gates that must pass before the deliverable is considered done).

### Progress Tracking & Decisions

**Single source of truth:** [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md)
- Updated whenever task status changes (complete, blocked, decision outcome, phase gate)
- No parallel trackers; check this one place for all status

**Developer authority:**
- If there is no blocker, proceed to the next step in the task sequence (you have authority)
- If blocked, escalate in chat: "I need human-derived input on [specific blocker]"
- See [GOVERNANCE_SOP.md](governance/GOVERNANCE_SOP.md) for escalation guidance

**Execution model (AI/developer):**
1. Read task specification
2. Execute the work
3. Create evidence artifacts
4. Update dashboard immediately
5. If blocked → escalate in chat with specific blocker

## Current Project Status

**E01 (Core Foundation):** ✅ COMPLETE (100%)  
**E02 (Ingestion + Library):** ✅ COMPLETE (all tasks + QC sign-offs)  
**E03 (Invoice Extraction Pipeline):** ✅ COMPLETE (surrogate QC satisfied)  
**E04 (Copilot Interface):** 🟡 IN PROGRESS (tests passing; UI/UX iteration ongoing)  
**E05 (Production Readiness):** ⏳ BLOCKED (awaiting E04 completion)

→ See [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) for detailed status.

---

## Definition of Done (DoD)

A Requirement is not complete until **all** of the following are satisfied:
- ✅ Meets all acceptance criteria
- ✅ Has tests implemented and passing (80%+ coverage target)
- ✅ Has evidence artifacts recorded (logs, screenshots, test results)
- ✅ Has documentation updated (README, onboarding, architecture)
- ✅ Passed external validation (QC or sponsor sign-off)
- ✅ Style Guide adherence verified (see docs/STYLE_GUIDE.md)

**Testing is mandatory. It is part of the development cycle, not optional.**

### Quality Gates (Governance)
- ❌ No epic begins without an epic kickoff document and sponsor approval
- ❌ No deliverable begins without requirement definitions
- ❌ No requirement is merged without DoD evidence and tests
- ❌ No task is signed off without linked evidence artifacts

**DoD enforcement is non-negotiable.** All gates must pass before advancing to the next phase.

## Custodial Work: Keeping the Repository Clean

The project root directory is the source of truth for governance and delivery artifacts. Temporary analysis files, working documents, and experimental outputs do not belong in the root.

### Guidelines for Temporary Files

**When you create temporary files** (analysis docs, working notes, diagnostic outputs, prototypes):

1. **Do not leave them in the root** – The root should contain only governance artifacts, navigation guides, and status dashboards
2. **Place them in the `burn-pile/` folder** – This folder is the holding area for:
   - Analysis documents created during research or decision-making
   - Working drafts that informed official deliverables
   - Diagnostic outputs and experimental explorations
   - Files that served their purpose but are no longer needed
3. **Include a README in `burn-pile/`** explaining what's there and why it's temporary
4. **Periodically review and remove** – When files in `burn-pile/` are no longer needed (decision made, analysis incorporated, etc.), delete them rather than letting them accumulate

### Examples

| Scenario | Action |
|----------|--------|
| Created an analysis comparing JD options for a task | Place in `burn-pile/JD_ANALYSIS_XXX.md` |
| Generated performance models during architecture planning | Place in `burn-pile/PerformanceModelExploration.md` |
| Built a reference matrix during governance design | Place in `burn-pile/GovernanceReferenceMatrix.md` |
| Tested a documentation structure before finalizing | Place in `burn-pile/StructureTest.md` |

After the decision is made or work is complete, the temporary file either:
- Gets consolidated into an official deliverable (then deleted from `burn-pile/`)
- Or is deleted entirely if no longer needed

**Principle:** Root cleanliness enforces clarity about what matters. Official artifacts stay in root; working artifacts use `burn-pile/`.

## Job Descriptions (JD) Integration

Every task is assigned to a specific Job Description (JD). The JD is embedded in the task filename and provides role clarity.

### How It Works
1. **Find your task** in `/roadmap/R01_LocalDocExtractionPlatform/epics/ExX/tasks/` 
2. **Task filename includes JD ID**, e.g., `T01.1.1_PM-001_RequirementsFile.md`
3. **Read the task spec** top-to-bottom for requirements and acceptance criteria
4. **Review your JD** in `/Setup/fiab/agents/job_descriptions/PM-001_Scoping_Agent.json` (or your assigned JD) to understand your role
5. **Execute the task** according to its acceptance criteria and DoD checklist

### Key JDs for This Project
| JD | Role | Primary Tasks |
|---|---|---|
| **PM-001** | Scoping Agent | Requirements gathering, documentation, scope clarity |
| **DEV-024** | Deliverables Manager | Orchestration, task decomposition, QA gating |
| **DEV-003** | Database Developer | Schema design, migrations, database infrastructure |
| **DEV-026** | Observability Engineer (Local Apps) | Telemetry, tracing, monitoring design |
| **DEV-004** | DevOps Engineer | CI/CD, containerization, deployment automation |
| **QC-101** | QA Engineer | External validation, acceptance testing, sign-off |
| **AGENT-002** | Prompt Systems Engineer | Extraction schemas, prompt design, evidence capture |
| **AGENT-004** | Agent Observability Lead | Agent instrumentation, tracing, debugging |

**Read your full JD definition before starting work.** The JD file contains your role's purpose, skills, and expected contributions.

---

## Operating Modes
- Batch mode: ingest/process many documents
- Focused mode: view one document with batch/corpus awareness
- Corpus mode: query historic documents tied to the same client/project

## Python Environment (Reproducible)

The repo does not store the virtual environment. Recreate it locally using:

- Create venv: `python -m venv .venv`
- Activate venv and install deps: `pip install -r requirements.txt`

The `requirements.txt` file is the canonical dependency list.

## Model & Runtime
- Local model runtime: Ollama
- Model selection: rule-based (context length, JSON reliability, GPU latency)
- Retrieval: local embeddings + SQL metadata + evidence pointers

## Ollama: Local-Only Chat (DocExtractor)

The backend can optionally use your local Ollama server for `/api/chat`.

### Quick smoke test (Ollama only)

- Verify Ollama is running: `curl -sS http://localhost:11434/api/tags | head`
- Run the repo smoke test:
   - `/Reserved/DocExtractor/.venv/bin/python scripts/ollama_smoke_test.py`

### Enable Ollama-backed `/api/chat`

The chat endpoint always stays **local-only**; non-local hosts are rejected.

Set env vars (examples):

- `DOCEXTRACTOR_OLLAMA_ENABLED=1`
- `DOCEXTRACTOR_OLLAMA_HOST=http://localhost:11434`
- `DOCEXTRACTOR_OLLAMA_MODEL=llama3.2:3b`
- `DOCEXTRACTOR_OLLAMA_TIMEOUT_S=60`
- `DOCEXTRACTOR_OLLAMA_WARMUP=1`
- `DOCEXTRACTOR_OLLAMA_MAX_LINES=40`
- `DOCEXTRACTOR_OLLAMA_MINI_SCHEMA=1`

Recommended defaults above ensure the invoice extraction pipeline uses the LLM path reliably with lower latency on local hardware.

If Ollama is unavailable (or errors), the backend gracefully falls back to a deterministic reply derived from extracted invoice fields.

### UI configuration

The UI reads its API base URL from `VITE_API_BASE_URL`.

- Example (recommended): create `ui/.env` from `ui/.env.example`
- Default fallback (if unset): `http://localhost:8000`

---

## Persistence (SQLite) — E02 Library Backbone

By default the API uses in-memory storage (good for development, cleared on restart).
Enable SQLite to persist documents, extractions, reviews, and corrections across restarts.

Env vars:
- `DOCEXTRACTOR_DB_ENABLED=1`
- `DOCEXTRACTOR_DB_PATH=/Reserved/DocExtractor/data/db/doc_extractor.sqlite3` (optional; default is under `data/db/`)

## Mixed-Document Ingestion (Invoices + Other Docs)

Use the generic ingest endpoint to build a mixed corpus:
- `POST /api/documents/ingest`

Client scoping (recommended):
- Provide `client_id` to ensure ingestion and corpus chat stay within a single client boundary.
- Example: `POST /api/documents/ingest?client_id=acme`

Client registry + strict selection:
- Known clients are managed via `GET /api/clients` and `POST /api/clients`.
- If the client registry is non-empty and a request does not include `client_id`, the server attempts to resolve a client from document text.
- If the server cannot confidently auto-assign a client, ingestion returns HTTP `409` with `detail.error="client_id_required"` and a `client_resolution` payload. In this case, retry with an explicit `client_id`.

Classification v1 assigns:
- `invoice` (runs invoice extraction and stores an extraction)
- `other` (stores metadata + a text excerpt for corpus context)

Document APIs:
- `GET /api/documents?limit=50&doc_type=invoice|other`
- `GET /api/documents/{document_id}`

## Batch Ingest (Resumable)

Use the CLI to ingest a folder of PDFs/TXTs with an on-disk progress file.

Command:
- `/Reserved/DocExtractor/.venv/bin/python scripts/batch_ingest.py /path/to/folder`

Defaults:
- API base: `http://127.0.0.1:8000` (local-only enforced)
- Endpoint: `/api/documents/ingest`
- Progress file: `<root>/.docextractor_ingest_progress.json`

Client scoping:
- If the server requires a client selection (HTTP `409 client_id_required`), the CLI will prompt once to select from `GET /api/clients`, then retry and reuse that selection for subsequent files.
- You can also pass `--client-id <id>` to avoid prompts (see `--help`).

Invoice-only mode:
- `/Reserved/DocExtractor/.venv/bin/python scripts/batch_ingest.py /path/to/folder --endpoint /api/invoices/extract`
