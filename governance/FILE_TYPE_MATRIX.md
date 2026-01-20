# FILE TYPE MATRIX — Exhaustive Reference

**Owner:** PM-007  
**Purpose:** Quick lookup: "I'm about to create [file type]. Where does it live, and what naming convention do I follow?"  
**Last Updated:** 2026-01-13  

---

## LOOKUP BY FILE TYPE

### GOVERNANCE & ANCHOR DOCS (Root Level)

| File Type | Specific Filename | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|-------------------|----------|-------|-------------|-------|---------|---------|
| Project Status Dashboard | `PROJECT_STATUS_DASHBOARD.md` | `/Reserved/DocExtractor/` | PM-007 | **FIXED** | No | Weekly EOD + milestone | Executive 2-min health snapshot (RAG per epic, blockers, decisions, next checkpoint) |
| Project README | `README.md` | `/Reserved/DocExtractor/` | PM-007 | **FIXED** | No | Epic kickoff | Project overview, vision, how to get started |
| Navigation Guide | `NAVIGATION_GUIDE.md` | `/Reserved/DocExtractor/` | PM-007 | **FIXED** | No | New epic | How to find anything: by role, by epic, by phase |
| Index | `INDEX.md` | `/Reserved/DocExtractor/` | PM-007 | **FIXED** | No | Monthly | Full inventory of docs (alphabetical + by category) |

### GOVERNANCE FRAMEWORK DOCS (/governance/)

| File Type | Specific Filename | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|-------------------|----------|-------|-------------|-------|---------|---------|
| Governance Overview | `GOVERNANCE_OVERVIEW.md` | `/governance/` | PM-007 | **FIXED** | No | Once (stable) | Framework: roadmap → epic → deliverable → requirement → task → JD → evidence hierarchy |
| File Placement Checklist | `FILE_PLACEMENT_CHECKLIST.md` | `/governance/` | PM-007 | **FIXED** | No | As needed | Where things go + pre-commit validation checklist |
| File Type Matrix | `FILE_TYPE_MATRIX.md` | `/governance/` | PM-007 | **FIXED** | No | As needed | This file: lookup by type |
| Governance SOP | `GOVERNANCE_SOP.md` | `/governance/` | PM-007 | **FIXED** | No | As needed | How we enforce governance (pre-commit, validation, escalation) |
| RAID Log | `RAID_LOG.md` | `/governance/` | PM-007 | **FIXED** | No | Continuous | Risks, assumptions, issues, dependencies (aggregate across epics) |
| Decision Log | `DECISION_LOG.md` | `/governance/` | PM-007 | **FIXED** | No | Event-driven | Every decision with options, chosen path, rationale, tradeoffs |
| Project Charter | `PROJECT_CHARTER.md` | `/charter/` | PM-007 | **FIXED** | No | Once | Vision, success criteria, constraints, authority boundaries, stakeholder roles |

### EPIC-LEVEL DOCS (/roadmap/.../epics/ExX_EpicName/)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Epic Definition | `epic.md` | `/roadmap/R01_LocalDocExtractionPlatform/epics/ExX_EpicName/` | Epic Lead | **FIXED: epic.md** | No | Once (or per scope change) | Epic goal, scope, 5 deliverables, timeline, team composition |
| **Summaries Subfolder → All Epic-Level Docs** |
| Executive Summary | `EXECUTIVE_SUMMARY.md` | `.../ExX_EpicName/summaries/` | Epic Lead | **FIXED** | No | Once per epic | 5-minute sponsor overview: goal, deliverables, DoD, success metrics, timeline |
| Task-JD Mapping | `TASK_JD_MAPPING.md` | `.../ExX_EpicName/summaries/` | Epic Lead | **FIXED** | No | Once per epic | All tasks mapped to JD roles with full context preloaded; coordination notes |
| Definition of Done | `DoD.md` | `.../ExX_EpicName/summaries/` | Epic Lead | **FIXED** | No | Once per epic | 8 mandatory quality gates per requirement (front-loaded, per R0X.1–R0X.5) |
| Kickoff Ready | `E0X_KICKOFF_READY.md` | `.../ExX_EpicName/summaries/` | Epic Lead | **E0X = epic number** | No | Once per epic | What's delivered, how to start, statistics, sign-off path for sponsor approval |
| Kickoff Summary | `E0X_KICKOFF_SUMMARY.md` | `.../ExX_EpicName/summaries/` | Epic Lead | **E0X = epic number** | No | Once per epic | Transition overview: what we designed, what we're about to execute |

### DELIVERABLE-LEVEL DOCS (/roadmap/.../epics/ExX_EpicName/deliverables/D0X.Y/)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Deliverable Spec | `deliverable.md` | `.../deliverables/D0X.Y_DeliverableName/` | Deliverable Owner | **FIXED: deliverable.md** | No | Per scope change | What is being delivered, which requirements it satisfies, acceptance criteria, owner |

### REQUIREMENT-LEVEL DOCS (/roadmap/.../epics/ExX_EpicName/requirements/R0X.Y/)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Requirement Spec | `requirement.md` | `.../requirements/R0X.Y_RequirementName/` | Requirement Owner | **FIXED: requirement.md** | No | Per scope change | Detailed requirement: what must be true, acceptance criteria, which tasks satisfy it, DoD checklist per requirement |

### TASK-LEVEL DOCS (/roadmap/.../epics/ExX_EpicName/tasks/)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Task Specification | `T0X.Y.Z_JD-NNN_[TaskName].md` | `.../tasks/` | JD-NNN (assigned) | **MUST INCLUDE JD-ID** | **YES** | Per execution | Task objective, acceptance criteria, DoD checklist, JD context preloaded, evidence links, blocking/blocked relationships |

### EXECUTION TRACKERS (Epic Tracking Folder)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Epic Execution Tracker | `E0X_EXECUTION_TRACKER.md` | `/roadmap/.../epics/E0X_EpicName/tracking/` | Epic Lead | **FIXED: E0X prefix** | No | Weekly during execution | All tasks, progress, blockers, critical path, DoD verification |
| Requirement Execution Tracker | `R0X.Y_EXECUTION_TRACKER.md` | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y/requirements/R0X.Y_RequirementName/` | Requirement Owner | **FIXED: R0X.Y prefix** | No | Weekly during execution | Tasks for this requirement, progress, blockers, completion checklist |
| Task Completion Evidence | `T0X.Y.Z_JD-NNN_[ArtifactType].md` | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y/requirements/R0X.Y_RequirementName/evidence/` | JD-NNN (task owner) | **MUST INCLUDE JD-ID + T reference** | **YES** | Per task completion | Validation reports, test results, code artifacts, docs, sign-offs, completion summary |

### REFERENCE & LOOKUP DOCS (/docs/)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Job Description Reference | `JD_[JD-ID]_[RoleName].md` | `/docs/` | PM-007 (curator) | **JD_[ID]_[Name]** | No | Per JD update | Full context for quick reference: skills, behaviors, world-class actions |
| Meeting Notes | `[Date]_[Meeting Type]_NOTES.md` | `/docs/meeting_notes/` | Attendee | **YYYY-MM-DD prefix** | No | Per meeting | Meeting notes linked from project timeline or sprint folder |
| Glossary | `GLOSSARY.md` | `/docs/` | PM-007 (curator) | **FIXED** | No | As needed | Project terminology, acronyms, definitions |
| Technical Documentation | `[Topic].md` (e.g., `API.md`, `ARCHITECTURE.md`, `DATABASE_SCHEMA.md`) | `/docs/` | DEV-xxx + QC-101 | **Topic-based** | No | Per release | Technical reference, decisions, design patterns |

### CODE & TESTS (/src/, /tests/)

| File Type | Filename Pattern | Location | Owner | Naming Rule | JD-ID | Refresh | Purpose |
|-----------|------------------|----------|-------|-------------|-------|---------|---------|
| Python Source Module | `[module_name].py` | `/src/[package]/` | DEV-xxx | **snake_case** | No | Continuous | Implementation code |
| TypeScript/JavaScript Source | `[module_name].ts` or `.js` | `/src/[package]/` | DEV-xxx | **camelCase or PascalCase per convention** | No | Continuous | Implementation code |
| Unit Tests | `test_[module].py` | `/tests/unit/` | QC-101 (lead) | **test_ prefix** | No | Continuous | Unit test coverage |
| Integration Tests | `test_[integration_name].py` | `/tests/integration/` | QC-101 (lead) | **test_ prefix** | No | Continuous | Integration test coverage |
| Acceptance Tests | `test_[feature].py` | `/tests/acceptance/` | QC-101 (lead) | **test_ prefix** | No | Continuous | Acceptance test coverage |

---

## QUICK DECISION TREE: WHERE DOES THIS GO?

```
START: I'm about to create a file. What type is it?

├─ GOVERNANCE ANCHOR? (Project health, navigation, governance framework)
│  └─ Goes to /governance/ or project root (PROJECT_STATUS_DASHBOARD.md only)
│     Owner: PM-007 | No JD-ID | Example: RAID_LOG.md
│
├─ EPIC-LEVEL SUMMARY? (Overview, mapping, DoD)
│  └─ Goes to /roadmap/.../epics/ExX/summaries/
│     Owner: Epic Lead | No JD-ID | Example: EXECUTIVE_SUMMARY.md, DoD.md
│
├─ TASK-LEVEL SPECIFICATION? (Actual work unit)
│  └─ Goes to /roadmap/.../epics/ExX/deliverables/D0X.Y/requirements/R0X.Y/tasks/
│     Owner: JD-NNN role | MUST INCLUDE JD-ID | Example: T02.1.1_JD-PM001_ScopeIngestLibrary.md
│
├─ EVIDENCE/PROOF OF WORK? (What was delivered + proof)
│  └─ Goes to /roadmap/.../epics/ExX/deliverables/D0X.Y/requirements/R0X.Y/evidence/
│     Owner: JD-NNN (task owner) | SHOULD INCLUDE JD-ID | Example: T02.1.1_JD-PM001_RequirementsScopingReport.md
│
├─ REFERENCE DOC? (How to use the project, glossary, JD context)
│  └─ Goes to /docs/ or /docs/meeting_notes/
│     Owner: PM-007 or DEV-xxx | No JD-ID | Example: JD_PM-001_ProjectManager.md, GLOSSARY.md
│
├─ CODE? (Implementation)
│  └─ Goes to /src/
│     Owner: DEV-xxx (per module) | No JD-ID | Example: ingest_service.py
│
├─ TEST? (Validation)
│  └─ Goes to /tests/
│     Owner: QC-101 (testing lead) | No JD-ID | Example: test_ingest_service.py
│
└─ SOMETHING ELSE?
   └─ STOP. Ask PM-007. Don't create until approved.
```

---

## NAMING CONVENTIONS AT A GLANCE

| Rule | Pattern | Examples | Counter-Examples |
|------|---------|----------|------------------|
| **Task files MUST have JD-ID** | `T0X.Y.Z_JD-NNN_[Name].md` | T02.1.1_JD-PM001_Scope.md | T02.1.1_Scope.md ❌ |
| **Evidence artifacts SHOULD have JD-ID** | `T0X.Y.Z_JD-NNN_[Type].md` | T02.1.1_JD-PM001_Report.md | T02.1.1_Report.md (less ideal) |
| **Epic summaries DO NOT have JD-ID** | `[Type]_[Name].md` | EXECUTIVE_SUMMARY.md | T02_PM-007_EXECUTIVE_SUMMARY.md ❌ |
| **Governance docs are fixed names** | Exact match | PROJECT_STATUS_DASHBOARD.md | Project_Status_Dash.md ❌ |
| **Deliverables/Requirements are fixed** | `deliverable.md`, `requirement.md` | deliverable.md | Deliverable_Spec.md ❌ |
| **Root level only for anchors** | `/[filename].md` only | /PROJECT_STATUS_DASHBOARD.md | /T02.1.1_Report.md ❌ |

---

## VALIDATION CHECKLIST (Quick Version)

Before creating a file, verify:

```
[ ] 1. File type exists in this matrix
[ ] 2. Home location is defined
[ ] 3. Naming convention matches
[ ] 4. JD-ID requirement is clear (Y/N)
[ ] 5. Owner can be named
[ ] 6. Refresh cycle is realistic
[ ] 7. At least one searchable link exists

PASS all 7 → Create the file
FAIL any → Ask PM-007 before creating
```

---

## HOW TO USE THIS DOCUMENT

**Scenario 1: "I'm creating a task specification for my work item"**
- Find "Task-Level Docs" row in the lookup table
- Location: `/roadmap/.../epics/ExX/tasks/`
- Naming: `T0X.Y.Z_JD-NNN_[TaskName].md` (JD-ID is required)
- Create file following that pattern

**Scenario 2: "I'm collecting validation evidence from my task completion"**
- Find "Task Completion Evidence" row in the lookup table
- Location: `/evidence/E0X/` or `/evidence/R0X.Y/`
- Naming: `T0X.Y.Z_JD-NNN_[ArtifactType].md` (JD-ID recommended)
- Location: `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y/requirements/R0X.Y.Z_RequirementName/evidence/`
- Naming:
   - Preferred for narrative artifacts: `T0X.Y.Z_<RoleToken>_[ArtifactType].md` where `<RoleToken>` is `JD-...` or a role like `DEV-024`, `PM-001`, `QC-101`, `AGENT-001`
   - Allowed for non-markdown artifacts: `.png`, `.pdf`, `.log`, `.txt`, etc. (store alongside the requirement evidence and link from the task/spec or evidence summary)
- Store there and link from the task file

**Scenario 3: "I'm creating an epic summary document"**
- Find "Executive Summary" row under "Epic-Level Docs"
- Location: `.../epics/ExX/summaries/`
- Naming: `EXECUTIVE_SUMMARY.md` (no JD-ID)
- Create file with that exact name

**Scenario 4: "I'm about to create a file but I don't see it in this matrix"**
- STOP
- Escalate to PM-007: "What type of file is this, and where should it live?"
- Update FILE_TYPE_MATRIX.md after PM decision is made

---

## VERSION HISTORY

| Date | Version | Change | Owner |
|------|---------|--------|-------|
| 2026-01-13 | 1.0 | Initial governance mapping | PM-007 |

**Next Review:** After E02 completion (validate against actual file creation patterns)
