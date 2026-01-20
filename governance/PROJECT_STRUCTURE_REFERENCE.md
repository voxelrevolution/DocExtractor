# PROJECT STRUCTURE REFERENCE

**Owner:** PM-007  
**Date:** 2026-01-13  
**Status:** GOVERNANCE STANDARD

---

## FOLDER HIERARCHY: WHERE THINGS LIVE

```
DocExtractor/
├── README.md (project overview)
├── governance/ (all governance docs)
│   ├── FILE_PLACEMENT_CHECKLIST.md
│   ├── FILE_TYPE_MATRIX.md
│   ├── GOVERNANCE_SOP.md
│   ├── PROJECT_STATUS_DASHBOARD.md
│   ├── DECISION_LOG.md
│   └── PROJECT_STRUCTURE_REFERENCE.md (this file)
│
├── roadmap/
│   └── R01_LocalDocExtractionPlatform/
│       ├── epics/
│       │   ├── E01_CoreFoundation/
│       │   │   ├── epic.md
│       │   │   ├── deliverables/
│       │   │   │   └── D01.1_DevEnvironmentSetup/
│       │   │   │       ├── deliverable.md
│       │   │   │       ├── requirements/
│       │   │   │       │   └── R01.1_DevEnvironmentReproducibility/
│       │   │   │       │       ├── requirement.md
│       │   │   │       │       ├── DoD.md
│       │   │   │       │       └── tasks/
│       │   │   │       │           ├── T01.1.1_PM-001_RequirementsFile.md
│       │   │   │       │           ├── T01.1.2_DEV-024_SetupScript.md
│       │   │   │       │           └── ...
│       │   │   │       │       └── evidence/ (task artifacts collected here)
│       │   │   │       │           └── T01.1.X_JD-___*.md
│       │   │   └── summaries/
│       │   │       ├── E01_EXECUTIVE_SUMMARY.md
│       │   │       ├── E01_TASK_JD_MAPPING.md
│       │   │       └── ...
│       │   │
│       │   ├── E02_IngestionLibrary/
│       │   │   ├── epic.md
│       │   │   ├── deliverables/
│       │   │   │   ├── D02.1_DocumentImporter/
│       │   │   │   │   ├── deliverable.md
│       │   │   │   │   ├── requirements/
│       │   │   │   │   │   ├── R02.1.1_ImportRequirements/
│       │   │   │   │   │   │   ├── requirement.md
│       │   │   │   │   │   │   ├── DoD.md
│       │   │   │   │   │   │   └── tasks/
│       │   │   │   │   │   └── R02.1.2_ImportEdgeCases/
│       │   │   │   │   │       ├── requirement.md
│       │   │   │   │   │       ├── DoD.md
│       │   │   │   │   │       └── tasks/
│       │   │   │   │   │   └── (each requirement also has an evidence/ folder co-located)
│       │   │   │   ├── D02.2_Deduplication/
│       │   │   │   │   ├── deliverable.md
│       │   │   │   │   ├── requirements/
│       │   │   │   │   └── evidence/
│       │   │   │   ├── D02.3_MetadataStore/
│       │   │   │   ├── D02.4_DocumentClassification/
│       │   │   │   └── D02.5_TaggingOrganization/
│       │   │   └── summaries/
│       │   │
│       │   ├── E03_InvoiceExtractionPipeline/
│       │   ├── E04_CopilotInterface/
│       │   └── E05_ProductionReadiness/
│       │
│       ├── research/ (research artifacts, notes, explorations)
│       └── archive/ (deprecated epics, old approaches)
│

Note: A root-level /evidence/ folder exists and may contain legacy or cross-epic artifacts
(e.g., onboarding validation logs). Canonical task evidence for current work is stored
under each requirement: `.../requirements/<R...>/evidence/`.
```

---

## FOLDER CONTENTS BY TYPE

### 🎯 Epic Folder (`E0X_EpicName/`)

**Contains:**
- `epic.md` – Epic goal, scope, timeline
- `deliverables/` – Folder containing all deliverables
- `summaries/` – Folder with executive summaries and mappings

**Responsibility:** Epic Lead

**Files NOT here:**
- ❌ Individual tasks (tasks live under requirements)
- ❌ Evidence (evidence lives under deliverable/evidence/)

---

### 📦 Deliverable Folder (`D0X.Y_DeliverableName/`)

**Contains:**
- `deliverable.md` – Deliverable objective, acceptance criteria, owner
- `requirements/` – Folder containing all requirements for this deliverable

**Canonical evidence location:** Evidence is stored under each requirement folder:
`requirements/<R...>/evidence/`.

**Legacy/exception:** Some historical deliverables may also include a deliverable-level
`evidence/` folder (e.g., `deliverables/<D...>/evidence/<R...>/...`). Treat this as legacy
unless a task spec explicitly instructs otherwise.

**Responsibility:** Deliverable Owner (usually DEV-024 or equivalent)

**What goes in each subfolder:**

#### `requirements/` subfolder
Contains one folder per requirement. Example: `R02.1.1_ImportRequirements/`


#### Evidence layout (canonical)
- Evidence lives inside the requirement folder:
  - Example: `requirements/R02.1.1_ImportRequirements/evidence/`
- Naming: `T0X.Y.Z_JD-NNN_[ArtifactType].md`

---

### 📋 Requirement Folder (`R0X.Y.Z_RequirementName/`)

**Contains:**
- `requirement.md` – Requirement definition, acceptance criteria, status
- `DoD.md` – Definition of Done checklist (8 mandatory gates)
- `tasks/` – Folder containing all tasks that satisfy this requirement

**Responsibility:** Requirement Owner (assigned JD role)

**Files in requirement.md:**
- Requirement definition and scope
- Acceptance criteria (what success looks like)
- Status: Not started | In progress | Complete | Blocked
- Link to evidence location: `../evidence/R0X.Y.Z_RequirementName/`

**Files in DoD.md:**
8 mandatory quality gates:
1. Specifications Complete – req spec written, reviewed, approved
2. Tasks Decomposed – all work broken into <4-hour tasks
3. Tests Written – unit, integration, acceptance tests defined
4. Code Coverage – minimum 80% coverage
5. Evidence Collected – test results, logs archived
6. Documentation Complete – all artifacts documented and linked
7. Validation Passed – QC-101 validated against acceptance criteria
8. No Technical Debt – blockers resolved, todos documented

**Sign-off checklist:**
- [ ] QC-101 External Validator confirms all 8 gates passed
- [ ] Deliverable Lead confirms acceptance criteria met
- [ ] Epic Owner (PM-007) records completion in PROJECT_STATUS_DASHBOARD.md

---

### ✅ Task Folder (`tasks/`)

**Contains:**
- Task spec files: `T0X.Y.Z_JD-NNN_TaskName.md`
- One file per task
- Created using TASK_SPECIFICATION_TEMPLATE.md

**Naming Convention:**
```
T0X.Y.Z_JD-NNN_TaskName.md

T = Task prefix
0X.Y.Z = Epic.Deliverable.Requirement.Task ID
JD-NNN = Job Description ID (assigned role)
TaskName = Human-readable task name
```

**Example:** `T02.1.1_JD-PM001_ScopeImportRequirements.md`

**What goes in task spec:**
1. Task objective and acceptance criteria
2. JD context (preloaded from job description)
3. Definition of Done (task-level gates)
4. Evidence artifacts expected (test results, logs, etc.)
5. How to mark task complete (checklist + sign-offs)

---

### 📁 Evidence Folder (`evidence/` inside the requirement folder)

**Contains:**
- Task execution artifacts organized by task
- Example files:
  - `T02.1.1_JD-PM001_RequirementSpec.md` (task output)
  - `T02.1.2_JD-DEV024_ImplementationCode.md` (task output)
  - `T02.1.3_JD-QC101_TestResults.md` (validation results)
  - `T02.1.4_JD-QC101_SignOff.md` (acceptance sign-off)

**Naming Convention:**
```
T0X.Y.Z_JD-NNN_[ArtifactType].md

T0X.Y.Z = Task ID
JD-NNN = Task owner (role that created artifact)
[ArtifactType] = What kind of artifact: Spec, Code, TestResults, SignOff, etc.
```

**What gets archived here:**
- ✅ Test results and logs
- ✅ Validation reports
- ✅ Design documents
- ✅ Code implementations
- ✅ Performance metrics
- ✅ QC sign-off documents
- ✅ Any artifact proving task completion

**What doesn't go here:**
- ❌ Source code (lives in `/src/` directory in main codebase)
- ❌ Current documentation (lives in requirement.md files)
- ❌ Task specifications (live in tasks/ folder)

---

## STRUCTURE CONSISTENCY ACROSS EPICS

**All epics follow the same structure:**
- Epic > Deliverables > Requirements > Tasks
- Each deliverable has corresponding evidence folder
- Each requirement has DoD.md and requirement.md
- Task files always named T0X.Y.Z_JD-NNN_Name.md

**Example paths are consistent:**
```
Epic 1:  E01_CoreFoundation/deliverables/D01.1_DevEnvironmentSetup/requirements/R01.1_DevEnvironmentReproducibility/tasks/T01.1.1_PM-001_RequirementsFile.md
Epic 2:  E02_IngestionLibrary/deliverables/D02.1_DocumentImporter/requirements/R02.1.1_ImportRequirements/tasks/T02.1.1_JD-PM001_ScopeImportRequirements.md
Epic 3:  E03_InvoiceExtractionPipeline/deliverables/D03.1_InvoiceTemplateBuilder/requirements/R03.1.1_InvoiceTemplates/tasks/T03.1.1_JD-NNN_*.md
```

**Every epic, every deliverable, every requirement follows the same pattern.**

---

## KEY PRINCIPLES

✅ **Flat vs. Nested:**
- NOT flat: Don't put all tasks at epic level
- NOT deeply nested: Don't put requirements inside deliverables inside tasks
- **CORRECT:** Epic > Deliverables > Requirements > Tasks (3 levels of hierarchy)

✅ **Evidence Organization:**
- Evidence mirrors requirement structure
- Evidence organized at deliverable level
- Evidence collected by task owner during execution
- Evidence stays organized by requirement ID

✅ **Naming Consistency:**
- All tasks start with T0X.Y.Z (Task ID)
- All tasks include JD-NNN (assigned role)
- All requirements documented in R0X.Y.Z folders
- All evidence organized under deliverable/evidence/

✅ **DoD Living Document:**
- DoD.md at every requirement level
- Same 8 gates for every requirement
- Sign-offs required: QC-101 + Deliverable Lead + PM-007

---

## AUTOMATION & GOVERNANCE INTEGRATION

This structure supports:
- **Automated task tracking** – each task has defined location
- **Evidence collection** – knows exactly where to look for R0X.Y.Z evidence
- **Validation** – can verify DoD gates by checking evidence location
- **Quality gates** – task won't mark complete without proper evidence
- **Escalation** – knows exactly where blockers live (in requirement evidence)

---

**Last Updated:** 2026-01-13  
**Authority:** PM-007  
**Status:** Aligned with all epics E01-E05
