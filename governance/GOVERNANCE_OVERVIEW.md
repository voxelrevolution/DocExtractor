# Project Governance Overview

## Purpose
This governance framework ensures that the Local Document Extraction Copilot is built with **clarity, traceability, and accountability**. Every deliverable is tracked to specific requirements, every requirement is traced to a job description, and every task has measurable acceptance criteria.

## Governance Hierarchy
```
Roadmap (R01)
    ├── Epic (E01–E05)
    │   ├── Deliverables (D01.1–D01.6)
    │   │   ├── Requirements (R01.1–R01.6)
    │   │   │   └── Tasks (T01.1.1–T01.1.6)
    │   │   │       └── Job Description ID (PM-001, DEV-024, etc.)
```

Each level builds on the previous with **explicit acceptance criteria** and **Definition of Done (DoD) gates**.

---

## Document Types & Where They Live

### 1. **Charter Documents** (`/charter/`)
**Purpose:** Foundational vision and governance model established at project kickoff.

- `CHARTER_01_ApplicationScope.md` – Original application scope, vision, and target users
- `CHARTER_02_RoadmapEpics.md` – Epic summary, sequencing, and high-level dependencies
- `CHARTER_03_GovernanceModel.md` – Governance framework, work decomposition, and Definition of Done
- `CHARTER_04_EpicKickoffTemplate.md` – Template for epic-level kickoff packages (used for E02 planning)

**Who reads these:** New team members, sponsors, architects. Reference these to understand **why** the project is structured the way it is.

---

### 2. **Roadmap & Epic Definitions** (`/roadmap/R01_LocalDocExtractionPlatform/`)

#### Master Roadmap (`roadmap.md`)
- 5-epic sequencing and critical path
- Epic success metrics and exit criteria
- Technology stack locked-in
- Non-negotiables (privacy, modularity, evidence)

#### Epic Folders (`/epics/E01–E05/`)
Each epic contains:
- `epic.md` – Epic objective, scope, deliverables, dependencies, timeline
- `/summaries/` – **All epic-level summary documents live here**
  - `EXECUTIVE_SUMMARY.md` – 5-minute sponsor overview
  - `TASK_JD_MAPPING.md` – Which job descriptions own which tasks
  - `KICKOFF_PACKAGE.md` – Full epic plan (tech stack, requirements, DoD)
  - `TEAM_QUICK_REFERENCE.md` – One-page team guide
  - `READY_FOR_KICKOFF.md` – Checklist that epic is ready to execute
  - `FINAL_VERIFICATION.md` – Exit criteria verification post-execution
- `/deliverables/` – Deliverable specs (D0X.Y)
- `/requirements/` – Requirement specs (R0X.Y)
- `/tasks/` – Task specs with JD IDs (T0X.Y.Z_JD-NNN)

**Canonical evidence location (current repo + automation):**
- Task evidence artifacts live under the requirement folder: `.../requirements/<R...>/evidence/`
- Task specifications live under: `.../requirements/<R...>/tasks/`

**Legacy/exception note:** Some historical content may use other evidence layouts (e.g.,
deliverable-level `deliverables/<D...>/evidence/<R...>/...` or root-level `/evidence/<R...>/...`).
Do not introduce new work using legacy layouts unless a task spec explicitly instructs it.

---

### 3. **Project-Level Documentation** (`/docs/`)
- `ONBOARDING.md` – 30-minute setup guide for new developers
- Supporting docs: architecture, API contracts, testing strategy, etc.

---

## Key Patterns for New Epics

### When creating a new epic (E02, E03, etc.):

1. **Create the epic directory structure:**
   ```
   /epics/ExX_EpicName/
       ├── epic.md                      (← Start here)
       ├── summaries/                   (← Create this folder)
       │   ├── EXECUTIVE_SUMMARY.md
       │   ├── TASK_JD_MAPPING.md
       │   └── ... (other summaries)
       ├── deliverables/
       │   └── DxX.Y_DeliverableName/
       │       ├── deliverable.md
       │       └── ...
       └── requirements/
           └── ... (same pattern)
   ```

2. **Update the roadmap.md** to reference the new epic.

3. **Create the EXECUTIVE_SUMMARY.md** early (before kickoff) for sponsor review.

4. **Populate TASK_JD_MAPPING.md** by reading the relevant JD definitions and mapping each task to the best-fit role.

---

## Definition of Done (DoD) Gates

Every deliverable must satisfy these before moving to the next epic:
- ✅ Requirement specs complete with acceptance criteria
- ✅ Tasks decomposed with JD assignments
- ✅ Tests written and passing (80%+ coverage)
- ✅ Code follows modularity standards (separation of concerns, reusable components)
- ✅ Evidence artifacts created (logs, traces, test results)
- ✅ Documentation updated (README, onboarding, architecture)
- ✅ Style Guide adherence verified (see docs/STYLE_GUIDE.md)
- ✅ External validation passed (QC sign-off, sponsor review)
- ✅ If no independent validator is available, a **surrogate external validation** may be performed by an AI adopting an approved **TEST JD** persona. This must be explicitly labeled as surrogate in the QC sign-off artifact and tracked in the epic tracker.

See `DoD.md` in each epic for detailed checklist.

---

## Governance Rules (Non-Negotiable)

1. **Every task must have a JD ID in its filename** (e.g., `T01.1.1_PM-001_RequirementsFile.md`)
2. **Every requirement must have explicit acceptance criteria**
3. **Every deliverable must have a Definition of Done checklist**
4. **No epic can advance without sponsor and external validation sign-off**
  - **Exception:** When a human validator is unavailable, the AI may act as external validator **only** by adopting a TEST JD persona and recording a **surrogate QC** sign-off (clearly labeled as surrogate) in the QC artifact and epic tracker.
5. **Modularity is the highest architectural priority** – every code contribution must respect layer separation

---

## For Project Leads & Sponsors

- **Status visibility:** See `PROJECT_STATUS_DASHBOARD.md` at the root for current epic status
- **Quick navigation:** See `NAVIGATION_GUIDE.md` to find any document fast
- **Epic summaries:** For a quick read on any epic, start with `/epics/ExX/summaries/EXECUTIVE_SUMMARY.md`
- **Decisions & approval:** All decisions are logged in each epic's `TASK_JD_MAPPING.md` and executive summary

---

## For Engineers & Task Owners

1. Find your task in `/epics/ExX/tasks/T0X.Y.Z_JD-YYY_TaskName.md`
2. Read the full task spec: objective, acceptance criteria, DoD checklist
3. Reference the linked JD definition to understand your role's expected contribution
4. Create/update artifacts in the `/evidence/` directory and link them in your task
5. When complete, mark task as done in the status dashboard

---

## For Architects & Tech Leads

- **Tech stack decisions:** See `roadmap.md` (locked in E01)
- **Modularity patterns:** See `/docs/ARCHITECTURE.md` and code examples in `/src/`
- **Code structure:** `/src/` mirrors the bounded contexts: `api/`, `database/`, `llm/`, `observability/`, `schemas/`

---

## Evolving This Framework

As the project progresses:
- Add new epics under `/epics/` (E06, E07, etc.)
- Create `/epics/ExX/summaries/` for each new epic
- Update `roadmap.md` and `PROJECT_STATUS_DASHBOARD.md` at key milestones
- Archive completed epics to `/archive/` when 100% complete and validated
