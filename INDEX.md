# DocExtractor – Complete Project Index

**Project:** Local Document Extraction Copilot  
**Status:** 🟢 E01 Ready for Kickoff  
**Last Updated:** 2026-01-13  

---

## 📋 Start Here

### For Project Sponsors (You)
1. **[E01 Executive Summary](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/EXECUTIVE_SUMMARY.md)** – 5-minute overview of what's ready
2. **[E01 Ready for Kickoff](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/READY_FOR_KICKOFF.md)** – Full E01 plan, tech stack, timeline
3. **[E01 Task-JD Mapping](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/TASK_JD_MAPPING.md)** – Why each task is assigned to its JD

### For Engineering Teams (Once Assigned)
1. **[docs/ONBOARDING.md](docs/ONBOARDING.md)** – Get your dev environment ready in <30 min
2. **[E01 Team Quick Reference](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/TEAM_QUICK_REFERENCE.md)** – Your role and tasks
3. **[Your task spec](#task-specifications)** – Detailed task acceptance criteria

### For Project Tracking & Navigation
- **[NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md)** – Find any document in seconds
- **[PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md)** – Live status of all work

---

## 🎯 Project Vision

**What:** A privacy-first, local-first desktop application that ingests financial documents and extracts structured data with a Copilot interface.

**Why:** Professionals in regulated environments need fast, accurate document data extraction that never touches the cloud.

**How:** GPU-accelerated local inference (Ollama), strong evidence pointers, human-in-the-loop workflows, modular Python backend, native desktop UI.

**Success (6 months):** Users save 50%+ time per document, extraction accuracy is 80–90%, regression tests prevent drift.

---

## 📐 Project Structure (Organized by Purpose)

```
/Reserved/DocExtractor/
├── charter/                              ← Project charter & founding documents
│   ├── CHARTER_01_ApplicationScope.md    (original vision & scope)
│   ├── CHARTER_02_RoadmapEpics.md       (epic sequencing & dependencies)
│   ├── CHARTER_03_GovernanceModel.md    (governance framework & work decomposition)
│   └── CHARTER_04_EpicKickoffTemplate.md (template for new epics)
│
├── governance/                           ← Governance rules & patterns
│   └── GOVERNANCE_OVERVIEW.md           (how governance works, rules, standards)
│
├── roadmap/
│   └── R01_LocalDocExtractionPlatform/
│       ├── roadmap.md                   (master roadmap: 5 epics, critical path)
│       └── epics/
│           ├── E01_CoreFoundation/
│           │   ├── epic.md
│           │   ├── summaries/            ← **All epic-level docs live here**
│           │   │   ├── EXECUTIVE_SUMMARY.md
│           │   │   ├── TASK_JD_MAPPING.md
│           │   │   ├── KICKOFF_PACKAGE.md
│           │   │   ├── TEAM_QUICK_REFERENCE.md
│           │   │   ├── READY_FOR_KICKOFF.md
│           │   │   └── FINAL_VERIFICATION.md
│           │   ├── deliverables/
│           │   └── requirements/
│           ├── E02_IngestionLibrary/
│           │   └── summaries/
│           ├── E03_InvoiceExtraction/
│           │   └── summaries/
│           ├── E04_EntityResolution/
│           │   └── summaries/
│           └── E05_CopilotInterface/
│               └── summaries/
│
├── docs/                                 ← Project-wide documentation
│   └── ONBOARDING.md                    (30-minute dev setup guide)
│
├── src/                                  ← Python codebase (modular)
│   ├── api/                             (FastAPI endpoints)
│   ├── database/                        (SQLAlchemy ORM, migrations)
│   ├── llm/                             (Ollama client, inference)
│   ├── observability/                   (OpenTelemetry tracing)
│   ├── schemas/                         (Pydantic models, validation)
│   └── main.py                          (FastAPI application)
│
├── tests/                                ← Test suite
├── scripts/                              ← Setup & utility scripts
├── evidence/                             ← Task artifacts, logs, test results
├── README.md                             ← Main project guide
├── NAVIGATION_GUIDE.md                   ← Find any document fast
├── PROJECT_STATUS_DASHBOARD.md           ← Live work status
├── INDEX.md                              ← You are here
└── docker-compose.yml                    ← Local dev environment
```

---

## 🔧 Tech Stack (Locked)

- **Language:** Python 3.11+
- **Backend API:** FastAPI
- **Desktop App:** Tauri + React
- **Database:** PostgreSQL 15 + pgvector
- **LLM Runtime:** Ollama + Mixtral 8x7b
- **Vector Embeddings:** sentence-transformers
- **Observability:** OpenTelemetry
- **Testing:** pytest + pytest-asyncio
- **CI/CD:** GitHub Actions

---

## 🚀 Roadmap & Epics

| Epic | Purpose | Timeline | Blocker? |
|------|---------|----------|----------|
| **E01** | Dev environment, Ollama, observability, schema | 2–3 weeks | YES – unblocks all |
| **E02** | File ingestion, deduplication, classification | 2–3 weeks | Blocked by E01 |
| **E03** | Invoice extraction, OCR, field validation | 3–4 weeks | Blocked by E02 |
| **E04** | Desktop UI, Copilot chat, export | 3–4 weeks | Blocked by E03 |
| **E05** | Performance, entity resolution, deployment | 2–3 weeks | Blocked by E04 |

---

## 📦 E01 Deliverables

| Deliverable | Status | Owner |
|-------------|--------|-------|
| **D01.1** – Dev Environment Setup | 🟡 Ready | DEV-024, DEV-003, PM-001 |
| **D01.2** – Ollama Integration | 🟡 Ready | DEV-009 |
| **D01.3** – Observability | 🟡 Ready | AGENT-004, DEV-026 |
| **D01.4** – Evidence Schema | 🟡 Ready | AGENT-002 |
| **D01.5** – Core Data Types | 🟡 Ready | DEV-003 |
| **D01.6** – CI/CD Pipeline | 🟡 Ready | DEV-004 |

---

## 📝 E01 Task Specifications (R01.1)

Six tasks, each with a JD assignment. Full specs in [roadmap/...E01_CoreFoundation/tasks/](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/):

1. **T01.1.1 – PM-001** – Create requirements.txt
   - Gather and pin all Python dependencies
   - Acceptance: All deps in requirements.txt with exact versions

2. **T01.1.2 – DEV-024** – Create scripts/setup.sh
   - Bootstrap automation for venv, deps, postgres, ollama
   - Acceptance: One script, <30 min execution, idempotent

3. **T01.1.3 – DEV-003** – Create docker-compose.yml
   - PostgreSQL service with pgvector, proper initialization
   - Acceptance: Service starts, health check passes, data persists

4. **T01.1.4 – PM-001** – Create docs/ONBOARDING.md
   - Step-by-step setup guide, troubleshooting, FAQ
   - Acceptance: Clear to non-technical users, no questions needed

5. **T01.1.5 – DEV-024** – Internal validation test
   - Run setup.sh end-to-end on fresh machine
   - Acceptance: No errors, all services running, <30 min total

6. **T01.1.6 – QC-101** – External validation test
   - Non-author follows onboarding, validates setup
   - Acceptance: External engineer signs off on reproducibility

---

## 🎓 Key Job Descriptions

All task files include JD references. Engineers must read their full JD before starting work:

| JD | Role | Link |
|---|---|---|
| **PM-001** | Scoping Agent | `/Setup/fiab/agents/job_descriptions/PM-001_Scoping_Agent.json` |
| **DEV-024** | Deliverables Manager | `/Setup/fiab/agents/job_descriptions/DEV-024_Deliverables_Manager.json` |
| **DEV-003** | Database Developer | `/Setup/fiab/agents/job_descriptions/DEV-003_Database_Developer.json` |
| **QC-101** | QA Engineer | `/Setup/fiab/agents/job_descriptions/QC-101_QA_Engineer.json` |

---

## ✅ Definition of Done (DoD)

Every requirement must satisfy its DoD before marking complete:
- ✅ Code artifacts created
- ✅ Documentation complete
- ✅ Tests passing (80%+ coverage target)
- ✅ External validation passed
- ✅ Evidence artifacts stored (logs, screenshots, test output)

Full DoD checklist: [roadmap/.../DoD.md](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/)

---

## 📊 Project Status

**Current Phase:** Kickoff – E01 Ready for Team Assignment

| Component | Status | Action |
|-----------|--------|--------|
| Roadmap & Charter | ✅ Complete | In `/charter/` |
| Governance Framework | ✅ Complete | See `GOVERNANCE_OVERVIEW.md` |
| E01 Scope & Planning | ✅ Complete | In `/epics/E01/summaries/` |
| Task Specifications | ✅ Complete | With JD IDs in filenames |
| Project Scaffolding | ✅ Complete | In `src/`, `tests/`, `scripts/` |
| Engineer Assignments | ⏳ Pending | Sponsor to assign 4 engineers |

---

## 🔐 Non-Negotiable Principles

1. **Private-by-Design** – Local inference only, no cloud
2. **GPU-First** – AI workloads optimized for GPU
3. **Evidence-Backed** – Every extraction has source pointers
4. **Governance-First** – Roadmap → Epic → Deliverable → Task (JD-assigned)
5. **Modular Codebase** – Clean separation of concerns, reusable components

---

## 📚 Quick Navigation by Role

### 👔 Sponsor / Business Lead
1. [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) – "As a Sponsor" section
2. [E01 Executive Summary](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/EXECUTIVE_SUMMARY.md)
3. [E01 Ready for Kickoff](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/READY_FOR_KICKOFF.md)

### 📋 Project Manager / Tech Lead
1. [GOVERNANCE_OVERVIEW.md](governance/GOVERNANCE_OVERVIEW.md) – Patterns & rules
2. [Charter Documents](charter/) – Foundational context
3. [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) – Daily tracking

### 👨‍💻 Engineer / Developer
1. [docs/ONBOARDING.md](docs/ONBOARDING.md) – Setup your machine
2. [E01 Team Quick Reference](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/TEAM_QUICK_REFERENCE.md) – Your role & tasks
3. Your task spec in `roadmap/.../tasks/T01.1.X_JD-YYY_...md`

### ✅ QA / External Validator
1. [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) – "As an External Validator" section
2. [E01 Final Verification](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/FINAL_VERIFICATION.md)
3. [DoD Checklist](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/)

---

## 🤝 How to Use This Project

### Step 1: Understand the Structure
- Read [README.md](README.md) (5 min) – Overall vision & non-negotiables
- Review [GOVERNANCE_OVERVIEW.md](governance/GOVERNANCE_OVERVIEW.md) (10 min) – How work flows

### Step 2: For Your Role
- **Sponsor:** See [E01 Executive Summary](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/EXECUTIVE_SUMMARY.md) & approve
- **Engineer:** Read [ONBOARDING.md](docs/ONBOARDING.md) & get your JD link from [E01 Team Quick Reference](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/TEAM_QUICK_REFERENCE.md)
- **PM/Lead:** Track in [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) & consult [GOVERNANCE_OVERVIEW.md](governance/GOVERNANCE_OVERVIEW.md)

### Step 3: Do Your Work
- Follow your task spec completely (it's the contract)
- Link to evidence in [evidence/](evidence/) folder
- Update [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) when done
- Request sign-off per DoD checklist

---

## 🆘 Help & Support

| Question | Where to Go |
|----------|------------|
| "Where do I find X document?" | [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) |
| "What does my role do?" | Read your JD (linked in your task file) |
| "What are the governance rules?" | [GOVERNANCE_OVERVIEW.md](governance/GOVERNANCE_OVERVIEW.md) |
| "What's my task exactly?" | Read your task file in `roadmap/.../tasks/` |
| "How do I set up my dev environment?" | [docs/ONBOARDING.md](docs/ONBOARDING.md) |
| "What's the current status?" | [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) |
| "What are the foundations of this project?" | [charter/](charter/) |

---

## 📌 Key Links Summary

| Document | Purpose | Link |
|----------|---------|------|
| Main Project Guide | Overview & non-negotiables | [README.md](README.md) |
| Find Any Document | Quick search by role & goal | [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) |
| Governance Framework | Rules, patterns, governance flow | [governance/GOVERNANCE_OVERVIEW.md](governance/GOVERNANCE_OVERVIEW.md) |
| E01 Summary Docs | Epic planning & kickoff | [roadmap/.../E01_CoreFoundation/summaries/](roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/) |
| Onboarding Guide | Dev environment setup | [docs/ONBOARDING.md](docs/ONBOARDING.md) |
| Live Status Tracker | Current work progress | [PROJECT_STATUS_DASHBOARD.md](PROJECT_STATUS_DASHBOARD.md) |
| Charter Documents | Foundational context & templates | [charter/](charter/) |

---

**Project Status:** ✅ Ready for Kickoff  
**Last Updated:** 2026-01-13  
**Prepared by:** Senior Technical Lead  

*Welcome to the Local Document Extraction Copilot project! All documentation is organized by purpose. Use [NAVIGATION_GUIDE.md](NAVIGATION_GUIDE.md) to find what you need fast.*
