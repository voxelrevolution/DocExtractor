# FILE PLACEMENT CHECKLIST & GOVERNANCE REFERENCE

**Owner:** PM-007 (Project Manager)  
**Last Updated:** 2026-01-13  
**Status:** GOVERNANCE STANDARD (Binding)  

---

## QUICK REFERENCE: WHERE DOES THIS GO?

**Use this table to find the home for any file you're about to create.**

| File Type | Home Location | Naming Convention | Owner | JD-ID Req? | Refresh Cycle | Purpose |
|-----------|---------------|-------------------|-------|-----------|---------------|---------|
| **PROJECT GOVERNANCE** |
| Project Status Dashboard | `/PROJECT_STATUS_DASHBOARD.md` (root) | PROJECT_STATUS_DASHBOARD.md | PM-007 | N | Weekly EOD + milestone | Stakeholder executive health snapshot |
| Navigation Guide | `/NAVIGATION_GUIDE.md` (root) | NAVIGATION_GUIDE.md | PM-007 | N | Every new epic | How to find anything in the project |
| README (Project Overview) | `/README.md` (root) | README.md | PM-007 | N | Every epic kickoff | What this project is, why it exists, how to start |
| INDEX | `/INDEX.md` (root) | INDEX.md | PM-007 | N | Monthly | Full inventory of all docs and where they live |
| **GOVERNANCE FRAMEWORK** |
| Governance Overview | `/governance/GOVERNANCE_OVERVIEW.md` | GOVERNANCE_OVERVIEW.md | PM-007 | N | Once (stable) | Framework: roadmap → epic → deliverable → task → JD hierarchy |
| File Placement Checklist | `/governance/FILE_PLACEMENT_CHECKLIST.md` | FILE_PLACEMENT_CHECKLIST.md | PM-007 | N | As needed | This document: where things go |
| File Type Matrix | `/governance/FILE_TYPE_MATRIX.md` | FILE_TYPE_MATRIX.md | PM-007 | N | As needed | Exhaustive file type → home mapping |
| Governance SOP | `/governance/GOVERNANCE_SOP.md` | GOVERNANCE_SOP.md | PM-007 | N | As needed | How we enforce: pre-commit, validation, escalation |
| RAID Log | `/governance/RAID_LOG.md` | RAID_LOG.md | PM-007 | N | Every meeting | Risks, assumptions, issues, dependencies (aggregate across epics) |
| Decision Log | `/governance/DECISION_LOG.md` | DECISION_LOG.md | PM-007 | N | Event-driven | Every decision with context, options, chosen path, rationale |
| Charter | `/charter/PROJECT_CHARTER.md` | PROJECT_CHARTER.md | PM-007 | N | Once | Vision, objectives, constraints, authority boundaries |
| **EPIC-LEVEL DOCS** |
| Epic Definition | `/roadmap/R01_LocalDocExtractionPlatform/epics/ExX_EpicName/epic.md` | epic.md | Epic Lead | N | Once (or per scope change) | Epic goal, scope, deliverables, timeline, owner |
| Epic Executive Summary | `/roadmap/.../epics/ExX_EpicName/summaries/EXECUTIVE_SUMMARY.md` | EXECUTIVE_SUMMARY.md | Epic Lead | N | Once per epic | 5-minute sponsor overview: goal, deliverables, success criteria, timeline |
| Epic Task-JD Mapping | `/roadmap/.../epics/ExX_EpicName/summaries/TASK_JD_MAPPING.md` | TASK_JD_MAPPING.md | Epic Lead | N | Once per epic | Task → JD assignments with full JD context preloaded |
| Epic Definition of Done | `/roadmap/.../epics/ExX_EpicName/summaries/DoD.md` | DoD.md | Epic Lead | N | Once per epic | Quality gates per requirement (8 mandatory gates upfront) |
| Epic Kickoff Ready Guide | `/roadmap/.../epics/ExX_EpicName/summaries/E0X_KICKOFF_READY.md` | E0X_KICKOFF_READY.md | Epic Lead | N | Once per epic | How to start: stats, mechanics, next steps for sponsor approval |
| Epic Summary (Post-Kickoff) | `/roadmap/.../epics/ExX_EpicName/summaries/E0X_KICKOFF_SUMMARY.md` | E0X_KICKOFF_SUMMARY.md | Epic Lead | N | Once per epic | Transition overview from design to execution |
| **DELIVERABLE-LEVEL DOCS** |
| Deliverable Spec | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/deliverable.md` | deliverable.md | Deliverable Owner | N | Per scope change | Deliverable goal, requirements it satisfies, acceptance criteria, owner |
| **REQUIREMENT-LEVEL DOCS** |
| Requirement Spec | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/requirement.md` | requirement.md | Requirement Owner | N | Per scope change | Requirement definition, acceptance criteria, tasks that satisfy it, DoD checklist |
| Requirement DoD | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/DoD.md` | DoD.md | Requirement Owner | N | Per scope change | 8 mandatory quality gates for this requirement (pre-defined template) |
| **TASK-LEVEL DOCS** |
| Task Specification | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/tasks/T0X.Y.Z_JD-NNN_TaskName.md` | T0X.Y.Z_JD-NNN_TaskName.md | JD-NNN (assigned role) | **YES** | Per execution | Task objective, acceptance criteria, DoD checklist, JD context, evidence links |
| **EVIDENCE & ARTIFACTS** |
| Requirement Evidence | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/evidence/` | [directory, not file] | Deliverable Owner | N | During execution | Collects all task execution artifacts: test results, logs, traces, validation reports |
| Task Evidence Artifact | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/evidence/T0X.Y.Z_JD-NNN_[Type].md` | T0X.Y.Z_JD-NNN_[Type].md | JD-NNN (task owner) | **YES** | Per execution | Evidence from task: TestResults, ValidationReport, SignOff, etc. |
| **EVIDENCE & ARTIFACTS** |
| Epic Execution Tracker | `/roadmap/.../epics/E0X_EpicName/tracking/E0X_EXECUTION_TRACKER.md` | E0X_EXECUTION_TRACKER.md | Epic Lead | N | Weekly during execution | Task progress, blockers, critical path status, DoD verification |
| Requirement Execution Tracker | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/R0X.Y_EXECUTION_TRACKER.md` | R0X.Y_EXECUTION_TRACKER.md | Requirement Owner | N | Weekly during execution | Task breakdown for this requirement, progress, blockers |
| Task Evidence Artifact | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/evidence/` | T0X.Y.Z_JD-NNN_[ArtifactType].md | JD-NNN (task owner) | **YES** | Per execution | Validation reports, test results, code artifacts, docs, signs-off |
| Evidence Summary File | `/roadmap/.../epics/E0X_EpicName/deliverables/D0X.Y_DeliverableName/requirements/R0X.Y.Z_RequirementName/evidence/` | T0X.Y.Z_JD-NNN_[ArtifactSummary].md | JD-NNN (task owner) | **YES** | Per completion | Links to all evidence, completion checklist, sign-offs |
| **REFERENCE & SEARCHABLE DOCS** |
| Job Description Reference | `/docs/JD_[JD-ID]_[RoleName].md` | JD_[JD-ID]_[RoleName].md | PM-007 (curator) | N | Per JD update | Full context of JD behaviors, skills, world-class actions (for quick lookup) |
| Glossary & Terminology | `/docs/GLOSSARY.md` | GLOSSARY.md | PM-007 (curator) | N | As needed | Project terminology, acronyms, definitions |
| **CODE & TECHNICAL ASSETS** |
| Source Code | `/src/` | module.py, service.ts, etc. | DEV-xxx (owner per module) | N | Continuous | Implementation code |
| Tests | `/tests/` | test_module.py, service.test.ts | QC-101 (testing lead) | N | Continuous | Unit, integration, acceptance tests |
| Documentation | `/docs/TECHNICAL.md`, `/docs/API.md`, etc. | [Topic].md | DEV-xxx + QC-101 | N | Per release | Technical reference, API docs, architecture decisions |

---

## PRE-COMMIT CHECKLIST

**Before you create or finalize ANY file, run through this checklist:**

```
FILE CREATION VALIDATION CHECKLIST
═══════════════════════════════════════════════════════════════

[ ] 1. PURPOSE: Can I articulate in one sentence why this file exists?
       (If not, don't create it.)

[ ] 2. HOME: Using the File Type Matrix above, does my file type have 
       a defined home? 
       (If not, escalate to PM-007 before creating.)

[ ] 3. NAMING: Does my filename follow the naming convention for this type?
       (Check the "Naming Convention" column above.)

[ ] 4. JD-ID: Does this file type require a JD-ID prefix?
       - If YES: Does my filename include it? (T0X.Y.Z_JD-NNN_TaskName.md)
       - If NO: Is my filename free of JD-ID? (No JD-NNN in file name)
       (If naming is wrong, fix before creating.)

[ ] 5. OWNER: Can I name the person responsible for maintaining this file?
       (If unclear, ask PM-007.)

[ ] 6. REFRESH CYCLE: Is my refresh cycle realistic and documented?
       (Weekly? Per milestone? Once per epic?)
       (Add this to the file as metadata, or document in RAID log if unclear.)

[ ] 7. REFERENCE: How will people find this file?
       - [ ] Linked from another doc? (Which one?)
       - [ ] Listed in INDEX.md?
       - [ ] Listed in NAVIGATION_GUIDE.md?
       (Ensure at least ONE reference path exists.)

[ ] 8. SEARCHABILITY: If someone searches for "[topic]" will they find it?
       - [ ] File title includes keyword?
       - [ ] File is linked from a search-friendly index?
       (If searchability is unclear, add to INDEX.md or a reference doc.)

[ ] 9. LIFECYCLE: Will this file be archived, deleted, or kept indefinitely?
       (Example: Task evidence artifacts are archived after epic complete; 
        PROJECT_STATUS_DASHBOARD is permanent; Kickoff guides archived per epic.)
       (If lifecycle is unclear, document in RAID log or ask PM-007.)

[ ] 10. VALIDATE AGAINST EXISTING: Does a similar file already exist?
        (Check FILE_TYPE_MATRIX and /evidence/ and /governance/ first.)
        (If yes, update existing instead of creating duplicate.)

═══════════════════════════════════════════════════════════════

If ANY checkbox fails, STOP. Escalate to PM-007 or revise before creating.

PASS = All 10 boxes checked ✅ → SAFE TO CREATE
FAIL = Any box unchecked ❌ → DO NOT CREATE (escalate)
```

---

## AUTOMATED GOVERNANCE CHECK (Run After Changes)

After reorganizations or new files, run:

- `scripts/governance_audit.py`

This flags:
- Duplicate deliverable prefixes (e.g., multiple `D02.5_*` folders)
- Missing `requirement.md` or `DoD.md`
- Non-conforming task/evidence filenames
- Empty `tasks/` or `evidence/` folders

---

## NAMING CONVENTIONS (DEFINITIVE RULES)

### Rule 1: Task Files MUST Include JD-ID

**Format:** `T[EPIC].[DELIVERY].[TASK]_JD-[ROLE]_[TaskDescription].md`

**Examples:**
- ✅ `T02.1.1_JD-PM001_ScopeIngestLocalLibrary.md`
- ✅ `T02.1.2_JD-DEV003_DatabaseSchema.md`
- ✅ `T02.2.1_JD-AGENT002_PromptOptimization.md`
- ❌ `T02.1.1_ScopeIngestLocalLibrary.md` (missing JD-ID)
- ❌ `T02.1.1_QC-101_T02.1.1_Validation.md` (duplicate T02.1.1)

**Why:** Every task is owned by a specific JD role. The filename makes ownership **visible and searchable** without opening the file.

---

### Rule 2: Epic-Level Docs DO NOT Include JD-ID

**Format:** `[DocType]_[Description].md` (no JD-ID)

**Examples:**
- ✅ `EXECUTIVE_SUMMARY.md`
- ✅ `TASK_JD_MAPPING.md`
- ✅ `DoD.md`
- ✅ `E02_KICKOFF_READY.md`
- ❌ `T02_PM-007_EXECUTIVE_SUMMARY.md` (JD-ID not needed for epic docs)

**Why:** Epic docs are authored by the epic lead but represent the entire epic team's agreement. JD-ID would imply sole responsibility when responsibility is collective.

---

### Rule 3: Evidence Artifacts SHOULD Include JD-ID

**Format:** `T[EPIC].[DELIVERY].[TASK]_JD-[ROLE]_[ArtifactType].md`

**Examples:**
- ✅ `T02.1.1_JD-PM001_RequirementsScopingReport.md`
- ✅ `T02.1.5_DEV-024_InternalValidationResults.pdf`
- ✅ `T02.1.6_QC-101_ExternalValidationCompletionNotice.md`
- ⚠️ `T02.1.5_ValidationResults.md` (missing JD-ID; okay but less traceable)

**Notes:**
- Evidence folders may contain non-Markdown artifacts (`.png`, `.pdf`, `.log`, `.txt`, etc.) when that is the most faithful representation of the work output.
- Role tokens may be either `JD-...` or a hyphenated role ID (e.g., `DEV-024`, `PM-001`, `QC-101`, `AGENT-001`) as used throughout this repository.

**Why:** Evidence artifacts show who completed the work. JD-ID makes it easy to audit "what did [role] deliver?"

---

### Rule 4: Root-Level Files Must Have Clear Governance Purpose

**Allowed at Project Root:**
- ✅ `README.md` (project overview)
- ✅ `NAVIGATION_GUIDE.md` (how to find things)
- ✅ `INDEX.md` (inventory of all resources)
- ✅ `PROJECT_STATUS_DASHBOARD.md` (executive health)
- ✅ Directories: `/roadmap/`, `/governance/`, `/evidence/`, `/src/`, `/tests/`, `/docs/`, `/scripts/`

**NOT Allowed at Project Root:**
- ❌ `E02_KICKOFF_READY.md` (belongs in epic/summaries/)
- ❌ `E02_KICKOFF_SUMMARY.md` (belongs in epic/summaries/)
- ❌ `R01.1_COMPLETION_NOTICE.md` (belongs in /evidence/R01.1/ with JD-ID)
- ❌ `MEETING_NOTES_2026-01-13.md` (belongs in /docs/meeting_notes/ or sprint folder)

**Rule:** If a file is specific to an epic, deliverable, requirement, or task, it lives in the epic hierarchy or evidence folder. Never at root.

---

## REFERENCE & DISCOVERABILITY

### How People Find Things (Searchable Index Chain)

**START HERE** for any search:

1. **PROJECT_STATUS_DASHBOARD.md** (root)
   - → Gives you project health + next checkpoint
   - → Links to NAVIGATION_GUIDE.md for detailed navigation

2. **NAVIGATION_GUIDE.md** (root)
   - → "I need to find [topic]"
   - → Organized by role, epic, phase, document type
   - → Links to specific files

3. **INDEX.md** (root)
   - → Exhaustive inventory of every doc (alphabetical + by category)
   - → Links to every file in the project
   - → Use when you need to browse everything

4. **GOVERNANCE_OVERVIEW.md** (/governance/)
   - → Understand the hierarchy and why it's organized this way
   - → Read once, reference never (unless on-boarding)

5. **FILE_TYPE_MATRIX.md** (/governance/)
   - → "What type of file am I looking for?" → Find its home
   - → Used when creating new files

6. **RAID_LOG.md** (/governance/)
   - → What are we tracking? What's at risk? What depends on what?
   - → Updated continuously during execution

7. **DECISION_LOG.md** (/governance/)
   - → Why was a decision made? What were the options?
   - → Prevents rehashing old decisions
   - → Explains tradeoffs

8. **Epic Folders** (/roadmap/.../epics/ExX/)
   - → epic.md → understand the epic scope
   - → /summaries/ → overview and task assignments
   - → /deliverables/ → what we're building
   - → /requirements/ → acceptance criteria
   - → /tasks/ → actual work with JD assignments

9. **Evidence Folders** (/roadmap/.../epics/ExX/deliverables/D0X.Y/requirements/R0X.Y/evidence/)
   - → Execution tracker → progress and blockers (in /tracking/)
   - → Task evidence → what was delivered and proof
   - → Sign-offs → who validated it?

---

## ESCALATION: What If I Don't Know Where It Goes?

**Ask in this order:**

1. **Check FILE_TYPE_MATRIX.md** — Is my file type listed?
2. **Check FILE_PLACEMENT_CHECKLIST.md** (this doc) — Do the naming rules apply?
3. **Ask PM-007** — "I need to create [file type]. Where does it live, and does it follow the naming convention?"

**PM-007 will:**
- [ ] Confirm or adjust the home location
- [ ] Confirm naming convention
- [ ] Update FILE_TYPE_MATRIX.md if this is a new file type
- [ ] Provide a written decision (documented in DECISION_LOG.md)

**Do not create the file until you have PM-007 approval.**

---

## LIFECYCLE & ARCHIVAL

Files follow a lifecycle:

| Lifecycle Phase | Duration | Status | Action |
|-----------------|----------|--------|--------|
| **CREATION** | At start of phase | 📝 ACTIVE | File created, linked from parent docs, added to INDEX.md |
| **MAINTENANCE** | During phase | 📝 ACTIVE | Updated per refresh cycle (weekly/milestone/continuous) |
| **COMPLETE** | At phase end | ✅ STABLE | No more updates; archived to /archive/ or versioned |
| **REFERENCE** | Indefinite (for some) | 📖 REFERENCE | Historical record; linked for context but not updated |
| **RETIRE** | Per decision | 🗑️ DELETED/ARCHIVED | Moved to /archive/ if historical value; deleted if no value |

**Example Lifecycle — Task Evidence Artifact:**
1. **CREATION**: Task assigned (T02.1.1 assigned to JD-PM001)
2. **MAINTENANCE**: Evidence collected as work progresses (weekly updates to task artifact)
3. **COMPLETE**: Task sign-off (T02.1.1_JD-PM001_CompletionEvidence.md finalized)
4. **REFERENCE**: Linked from requirement completion summary; available for audit
5. **RETIRE** (Optional): After epic complete, archived to /archive/E02/ for historical record

**Example Lifecycle — PROJECT_STATUS_DASHBOARD.md:**
1. **CREATION**: Project starts
2. **MAINTENANCE**: Updated every Friday EOD + milestone
3. **COMPLETE**: Never (continuous governance)
4. **REFERENCE**: Always current; historical versions archived separately
5. **RETIRE**: At project end (archived as project close-out artifact)

---

## SUMMARY: THE ONE-PARAGRAPH RULE

**Every file must answer these four questions:**
1. **Purpose**: Why does this exist? (One sentence)
2. **Home**: Where does it live? (Path from FILE_TYPE_MATRIX.md)
3. **Owner**: Who maintains it? (Name and JD-ID if applicable)
4. **Refresh**: How often is it updated? (Once, weekly, per milestone, continuous)

If you can't answer all four, the file doesn't need to exist yet.

---

## VERSION HISTORY

| Date | Version | Change | Owner |
|------|---------|--------|-------|
| 2026-01-13 | 1.0 | Initial governance standard | PM-007 |

**Next Review:** After E02 completion (validate against actual usage)
