# E02 Executive Summary – Ingestion + Local Library
**Project:** Local Document Extraction Copilot  
**Epic:** E02 – Ingestion + Local Library (Batch Import & Organization)  
**Status:** 🟡 Ready for Kickoff  
**Date:** 2026-01-13  

---

## Epic Goal
Create a reliable, resumable, and auditable local document library that supports batch import, deduplication, classification, and metadata storage for downstream extraction and Copilot workflows.

---

## What E02 Delivers (5 Deliverables)

| Deliverable | Owner | Goal | Key Output |
|-------------|-------|------|-----------|
| **D02.1** – Document Importer | DEV-024 | Batch + single file ingestion | Import engine supporting PDF, XLSX, DOCX, images |
| **D02.2** – Deduplication | DEV-003 | Detect & handle duplicate documents | Hashing + match algorithm with audit trail |
| **D02.3** – Metadata Store (SQL) | DEV-003 | SQL schema for document library | PostgreSQL schema + migrations + indices |
| **D02.4** – Classification v1 | AGENT-002 | Document type classification | Classifier for invoice/contract/other categories |
| **D02.5** – Tagging & Organization | DEV-024 | User document organization | Tag system + grouping by client/project/batch |

---

## Definition of Done – Front-Loaded ✅

**Every deliverable MUST satisfy all criteria before merging:**

- [x] **Requirement Specs Complete** – All acceptance criteria defined upfront (see TASK_JD_MAPPING.md)
- [x] **Tasks Decomposed** – Each requirement broken into <4-hour tasks with JD assignments
- [x] **Job Descriptions Preloaded** – Every task spec includes full JD context (skills, behaviors, output expectations)
- [x] **Tests Implemented** – Minimum 80% code coverage; tests written BEFORE implementation
- [x] **Evidence Artifacts** – Test results, logs, and traces collected in `/evidence/E02/`
- [x] **Documentation Updated** – README, schema diagrams, API docs updated for each deliverable
- [x] **External Validation Passed** – QC engineer validates against acceptance criteria; sponsor sign-off
- [x] **No Technical Debt** – Code follows modularity patterns; no workarounds or shortcuts

**DoD is not optional. It is the entry & exit gate for each requirement.**

---

## Scope In / Out

### ✅ In Scope
- Single + batch file import (PDF, XLSX, DOCX, PNG/JPG)
- Document hashing and deduplication
- Basic metadata extraction (name, size, type, date)
- Document classification (invoice/contract/other)
- SQL schema + migrations for library storage
- Progress tracking & resumability (batch restart)
- Tagging + grouping (client, project, batch ID)

### ❌ Out of Scope
- Invoice field extraction (that's E03)
- Copilot chat UI (that's E04)
- Advanced OCR (deferred to E03)
- Cloud storage (always local/offline)
- Full-text search (later optimization)

---

## Job Descriptions (JD) Assigned

**How to Use:** Every task filename includes JD-ID. Read your JD file in `/Setup/fiab/agents/job_descriptions/` to understand your role.

| JD ID | Role | E02 Responsibility | Hours |
|-------|------|-------------------|-------|
| **DEV-024** | Deliverables Manager | D02.1 (lead), D02.5 (lead), task coordination | 30–40 |
| **DEV-003** | Database Developer | D02.2 (lead), D02.3 (lead), schema design | 25–35 |
| **AGENT-002** | Prompt Systems Engineer | D02.4 (lead), classification prompts + eval | 15–20 |
| **PM-001** | Scoping Agent | Requirement review + DoD enforcement | 10–15 |
| **QC-101** | External Validator | Acceptance testing + sign-off | 10–15 |

---

## Critical Dependencies

**E02 depends on:**
- ✅ **E01 Complete** – All 6 deliverables + tests passing
- ✅ **Development environment ready** – Python 3.12, PostgreSQL, Ollama available
- ✅ **Tech stack locked** – FastAPI, SQLAlchemy, Pydantic finalized in E01

**E02 unblocks:**
- 🟡 **E03** – Invoice Extraction Pipeline (requires D02.1, D02.3, D02.4)

---

## Success Criteria (MVP Gate)

All deliverables must achieve these outcomes:

- ✅ Batch import handles **>100 files** without errors
- ✅ Deduplication **is 100% correct** and fully auditable
- ✅ Metadata queries **complete in <100ms** for typical batches (1K docs)
- ✅ Document classification **achieves 90%+ accuracy** on test set
- ✅ Progress tracking **survives process restart** (resumability verified)
- ✅ All **tests pass** with 80%+ code coverage
- ✅ All **DoD requirements met** (evidence, docs, validation)

---

## Timeline & Milestones

| Milestone | Target | Owner | Blocker? |
|-----------|--------|-------|----------|
| **E02 Kickoff** | 2026-01-13 | PM-001 | — |
| **D02.1 Complete** | 2026-01-27 | DEV-024 | Critical for D02.2, D02.4 |
| **D02.2, D02.3 Complete** | 2026-02-03 | DEV-003 | Critical for D02.5 |
| **D02.4 Complete** | 2026-01-27 | AGENT-002 | Can start after tests written |
| **D02.5 Complete** | 2026-02-10 | DEV-024 | Depends on D02.1, D02.3 |
| **All Tests Passing** | 2026-02-10 | QC-101 | Hard stop for E02 exit |
| **External Validation** | 2026-02-17 | QC-101 | Sponsor sign-off |
| **E02 Exit Gate** | 2026-02-17 | Tech Lead | Unblocks E03 |

**Critical Path:** D02.1 → D02.5 (depends on import + schema)

---

## Risk & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Batch import performance regression | HIGH | Implement load testing (<100ms for 1K docs) from day 1 |
| Dedup false negatives (miss duplicates) | HIGH | Create reference test set; unit test every edge case |
| PostgreSQL schema blocking | MEDIUM | Pre-design + review schema with DEV-003 by 2026-01-20 |
| Classification accuracy drift | MEDIUM | Track metrics weekly; re-run eval suite on each change |
| Database migrations failing in production | HIGH | Test all migrations on fresh DB before merging |

---

## Tools & Tech Stack

**Inherited from E01 (Locked):**
- Language: Python 3.12
- Framework: FastAPI 0.109.0
- Database: PostgreSQL 15 + pgvector 0.2.0
- ORM: SQLAlchemy 2.0.23
- Schema versioning: Alembic
- Testing: pytest 7.4.3 + pytest-asyncio 0.21.1
- LLM: Ollama 0.11.7 with Mixtral 8x7b

**New E02 Tools:**
- Document processing: python-pptx, openpyxl, pdf2image
- Hashing: hashlib (built-in)
- Classification: Prompt-based via Ollama (no new ML frameworks)

---

## Document Map

| Document | Purpose |
|----------|---------|
| [E02 Executive Summary](EXECUTIVE_SUMMARY.md) | This document |
| [Task-JD Mapping](TASK_JD_MAPPING.md) | Assignment rationale + full JD context |
| [Kickoff Package](KICKOFF_PACKAGE.md) | Full E02 plan + deliverables + requirements |
| [Team Quick Reference](TEAM_QUICK_REFERENCE.md) | One-page per-engineer guide |
| [DoD Checklist](DoD.md) | Requirement-by-requirement DoD checklist |
| [Deliverable Specs](../deliverables/) | D02.1–D02.5 detailed specs |
| [Requirement Specs](../requirements/) | R02.1–R02.5 detailed specs |
| [Task Specs](../tasks/) | T02.X.Y_JD-ZZZ_TaskName.md |

---

## Sponsor Decision Point

### ❓ Ready to Approve E02 Kickoff?

**Confirm before team assignment:**

- [ ] **Scope** – In/Out scope clearly defined? Any gaps?
- [ ] **Timeline** – 2–3 weeks acceptable?
- [ ] **Team** – Assign engineers to JD roles (DEV-024, DEV-003, AGENT-002)?
- [ ] **DoD** – Definition of Done is non-negotiable? Understood?
- [ ] **Budget** – ~100 hours of engineering time available?

**Once approved:**
1. Assign team members to JD roles
2. Share [TASK_JD_MAPPING.md](TASK_JD_MAPPING.md) with assigned engineers
3. Kickoff meeting: walk team through deliverables + DoD
4. Engineers begin task execution (T02.X.Y files)

---

## Key Principles

✅ **DoD is upfront, not an afterthought**
✅ **Every task preloads its JD (skills, behaviors, outputs)**
✅ **Evidence artifacts mandatory before merge**
✅ **Tests written before code**
✅ **External validation required**
✅ **No tech debt shortcuts**

---

**Status:** ✅ Ready for Sponsor Sign-Off  
**Date:** 2026-01-13  
**Next Action:** Sponsor review → team assignment → task execution

