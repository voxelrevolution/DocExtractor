# TASK SPECIFICATION TEMPLATE

**Purpose:** Every task created uses this template. Governance rules are embedded in task definition, not separate.

**Template Instructions:**
1. Copy this template for each new task
2. Fill in [TASK_ID], [JD_ID], [Task Name], [Description], etc.
3. The file name, location, and artifact naming are **specified in the template** (not chosen by developer)
4. Task creator and assigned JD role receive the spec as-is; no validation needed

---

## Task Specification

**Task ID:** T[EPIC][DELIVERY][TASK]_JD-[ROLE]_[TaskName]

**Example: T02.1.1_JD-PM001_ScopeIngestLocalLibrary**

---

### SECTION 1: GOVERNANCE (EMBEDDED)

**This section specifies where files go. Developers follow it exactly.**

#### Task Deliverable (Specification File)

| Property | Value |
|----------|-------|
| **File Name** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_[TaskName].md |
| **Example** | T02.1.1_JD-PM001_ScopeIngestLocalLibrary.md |
| **Location** | /roadmap/R01_LocalDocExtractionPlatform/epics/E[EPIC]_[EpicName]/tasks/ |
| **Owner** | [ROLE] (non-delegable) |
| **Purpose** | Task specification + acceptance criteria + DoD checklist |

**Completion Requirement:** This file MUST exist in the specified location with the specified name for task to be marked complete.

---

#### Evidence Artifacts (Created as Task Progresses)

| Artifact Type | File Name Pattern | Location | Owner | Purpose |
|---------------|-------------------|----------|-------|---------|
| **Scoping Report** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_ScopingReport.md | /evidence/R[EPIC][DELIVERY]/ | [ROLE] | Initial scope definition |
| **Design Document** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_Design.md | /evidence/R[EPIC][DELIVERY]/ | [ROLE] | Technical approach |
| **Implementation Notes** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_Implementation.md | /evidence/R[EPIC][DELIVERY]/ | [ROLE] | Work progress notes |
| **Test Results** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_TestResults.md | /evidence/R[EPIC][DELIVERY]/ | [ROLE] | Validation evidence |
| **Completion Summary** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_CompletionSummary.md | /evidence/R[EPIC][DELIVERY]/ | [ROLE] | What was delivered |
| **Sign-Off** | T[EPIC][DELIVERY][TASK]_JD-[ROLE]_SignOff.md | /evidence/R[EPIC][DELIVERY]/ | [VALIDATOR] | QC-101 approval |

**Artifact Creation:** Not all artifacts are required upfront. Create them as work progresses. Each artifact follows the naming pattern above.

**Completion Requirement:** All created artifacts MUST have names matching the pattern above. Evidence goes in /evidence/R[EPIC][DELIVERY]/ (tied to the requirement this task satisfies).

---

### SECTION 2: TASK DEFINITION

**Fill in these fields. Everything else is auto-specified above.**

#### Objective (One Sentence)

[What is this task trying to achieve?]

**Example:** Scope the local document ingestion system, document stakeholder requirements, and secure sponsor approval to proceed with implementation.

---

#### Description

[What work needs to be done? Who is doing it? Why does it matter?]

**Example:**
- Interview key stakeholders (PM-001 responsibility)
- Document what documents we ingest (file types, volume, metadata)
- Define what "local" means (on-device, no cloud, air-gapped options)
- Document constraints (storage limits, performance targets, compliance)
- Present to sponsor for approval (go/no-go decision)
- Document decision and next steps

---

#### Acceptance Criteria

[What does DONE look like?]

**Format:** Use task completion checklist below (section 5)

---

#### Assigned JD Role

**Role:** [ROLE Name] (e.g., PM-001 = Project Manager)

**Assignment Details:**
- Role is non-delegable (PM-001 is responsible, full stop)
- All artifacts produced by this task are owned by this role (JD-ID in file names)
- Role has final authority on task completion (no hand-offs)

---

#### Dependencies (Blocking This Task)

[What must be complete before this task starts?]

**Example for T02.1.1:**
- T01.1.6 (E01 external validation) ← must complete first
- No other dependencies

**Example for T02.1.2:**
- T02.1.1 (scoping) ← must complete first
- R02.1 requirement spec ← must be finalized

---

#### Downstream Tasks (That This Unblocks)

[What tasks can't start until this one is done?]

**Example for T02.1.1:**
- T02.1.2_JD-DEV003_DatabaseSchema (blocked until scope approved)
- T02.2.1_JD-DEV024_IngestPipeline (blocked until scope approved)

---

### SECTION 3: ACCEPTANCE CRITERIA & DEFINITION OF DONE

**These are the 8 mandatory quality gates for this task's requirement.**

Requirement: **R[EPIC][DELIVERY]** (e.g., R02.1 = Scope Import Requirements)

#### DoD Checklist (8 Gates)

Developers check these boxes as work progresses. All must be checked before task completion.

- [ ] **Gate 1: Specification Complete** – Task spec file created with full acceptance criteria
- [ ] **Gate 2: Approach Defined** – Design documented (how we'll solve this)
- [ ] **Gate 3: Implementation Complete** – Code/work finished; no TODOs left
- [ ] **Gate 4: Testing Verified** – All acceptance criteria have test evidence
- [ ] **Gate 5: JD Context Embedded** – [ROLE] context fully documented in task spec
- [ ] **Gate 6: Artifacts Collected** – All evidence files created and properly named
- [ ] **Gate 7: Documentation Updated** – All design/API/process docs updated
  - Style Guide adherence review recorded (docs/STYLE_GUIDE.md)
- [ ] **Gate 8: External Validation Approval** – Validator has reviewed and signed off (T[EPIC][DELIVERY][TASK]_JD-QC101_SignOff.md)
  - If QC-101 is unavailable, a surrogate validator may be used **only** by adopting an approved TEST JD persona. The sign-off must be labeled **Surrogate QC** and recorded in the epic tracker.

**Completion:** Task is done when all 8 gates are checked AND external validation signs off (QC-101 or authorized surrogate).

---

### SECTION 4: JD CONTEXT (PRELOADED)

**This section tells [ROLE] what we expect from them. Full context from their job description.**

#### Role: [ROLE NAME]

**Agent ID:** [JD-ID] (e.g., PM-001)

**Key Responsibilities for This Task:**
[Pull from JD definition: what is this role accountable for?]

**Example for PM-001 (Project Manager) on T02.1.1:**
- Clarify objectives and acceptance criteria with stakeholder
- Translate scope into executable work
- Identify dependencies and risks
- Secure stakeholder approval (go/no-go decision)
- Document decisions and rationale

**World-Class Behaviors Expected:**
[From JD definition: what does excellence look like?]

**Example for PM-001:**
- Scope is crystal clear (no ambiguity)
- Scope is achievable within constraints
- Stakeholder is aligned and has approved
- Risks are identified and mitigated
- Next steps are obvious

**Output Expectations:**
- Task spec file (T02.1.1_JD-PM001_ScopeIngestLocalLibrary.md)
- Scoping report with stakeholder input (T02.1.1_JD-PM001_ScopingReport.md)
- Sponsor approval document (T02.1.1_JD-PM001_Approval.md)
- Risk/assumption log for this requirement

---

### SECTION 5: EVIDENCE COLLECTION CHECKLIST

**As work progresses, create artifacts following the pattern in Section 1.**

**Artifacts to Create (Suggested):**

- [ ] Task Spec File
  - File: T[EPIC][DELIVERY][TASK]_JD-[ROLE]_[TaskName].md
  - Location: /roadmap/.../tasks/
  - Content: This task specification document (updated as work progresses)

- [ ] Scoping/Design Document
  - File: T[EPIC][DELIVERY][TASK]_JD-[ROLE]_ScopingReport.md
  - Location: /evidence/R[EPIC][DELIVERY]/
  - Content: What we learned, decisions made, next steps

- [ ] Implementation Work
  - File: T[EPIC][DELIVERY][TASK]_JD-[ROLE]_Implementation.md
  - Location: /evidence/R[EPIC][DELIVERY]/
  - Content: How we solved it, code snippets, design rationale

- [ ] Testing/Validation
  - File: T[EPIC][DELIVERY][TASK]_JD-[ROLE]_TestResults.md
  - Location: /evidence/R[EPIC][DELIVERY]/
  - Content: Proof that acceptance criteria are met

- [ ] Completion Summary
  - File: T[EPIC][DELIVERY][TASK]_JD-[ROLE]_CompletionSummary.md
  - Location: /evidence/R[EPIC][DELIVERY]/
  - Content: What was delivered, what's next, blockers/risks

- [ ] QC-101 Sign-Off
  - File: T[EPIC][DELIVERY][TASK]_JD-QC101_SignOff.md
  - Location: /evidence/R[EPIC][DELIVERY]/
  - Content: Validator confirms DoD gates passed; task approved

**Note:** Not all artifacts are required. Create them as makes sense for the work. The pattern is the guide.

---

### SECTION 6: HOW TO START THIS TASK

**Step 1: Review This Spec**
- [ ] Read all sections above
- [ ] Confirm you understand objective, acceptance criteria, dependencies

**Step 2: Check Dependencies**
- [ ] Confirm blocking tasks are complete
- [ ] If blocked, report it to PROJECT_STATUS_DASHBOARD.md

**Step 3: Create Task Spec File**
- [ ] Create file: T[EPIC][DELIVERY][TASK]_JD-[ROLE]_[TaskName].md
- [ ] Location: /roadmap/R01_LocalDocExtractionPlatform/epics/E[EPIC]_*/tasks/
- [ ] Content: Copy this template; fill in your details; update as work progresses
- [ ] Once created, link it from requirement tracker

**Step 4: Begin Work**
- [ ] Work according to acceptance criteria
- [ ] Create evidence artifacts as you progress
- [ ] Link evidence from task spec file

**Step 5: Report Status**
- [ ] Update task spec with progress
- [ ] If you hit a blocker, update PROJECT_STATUS_DASHBOARD.md immediately
- [ ] If you hit a blocker, update E0X_EXECUTION_TRACKER.md immediately
- [ ] If you need a decision, post it to PROJECT_STATUS_DASHBOARD.md
- [ ] If you need a decision, post it to E0X_EXECUTION_TRACKER.md

**Step 6: Request Validation**
- [ ] When DoD gates are complete, request QC-101 sign-off
- [ ] QC-101 creates: T[EPIC][DELIVERY][TASK]_JD-QC101_SignOff.md
- [ ] Once signed, task is complete

---

### SECTION 7: HOW TO MARK TASK COMPLETE

**Completion Criteria:**

- [ ] All 8 DoD gates checked
- [ ] All evidence artifacts created and properly named
- [ ] All artifacts linked from task spec file
- [ ] QC-101 sign-off obtained
- [ ] Requirement tracker updated
- [ ] PROJECT_STATUS_DASHBOARD.md updated with task completion + timestamp
- [ ] E0X_EXECUTION_TRACKER.md updated with task completion + status change

**Task is DONE when all above are true.**

---

## EXAMPLE: FULLY FILLED-IN TASK SPEC

See: [T02.1.1_JD-PM001_ScopeIngestLocalLibrary_EXAMPLE.md](/roadmap/R01_LocalDocExtractionPlatform/epics/E02_IngestionLibrary/tasks/T02.1.1_JD-PM001_ScopeIngestLocalLibrary_EXAMPLE.md)

(This example task spec shows what a complete task looks like.)

---

## KEY PRINCIPLE

**Governance is embedded, not enforced retroactively.**

When you receive a task:
- File location is specified ✅ (no choices)
- File naming is specified ✅ (no choices)
- Artifact pattern is specified ✅ (no choices)
- Acceptance criteria are specified ✅ (no ambiguity)
- Evidence artifacts are specified ✅ (no guessing)

You don't run a checklist and validate compliance. **You follow the spec.**

If you deviate, you're not complying with the task assignment itself—which is impossible because the task assignment IS your work order.

---

**Version:** 1.0  
**Owner:** PM-007 (Project Manager)  
**Effective:** 2026-01-13  
**Status:** Standard template for all tasks in epics E02–E05
