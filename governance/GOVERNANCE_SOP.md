# Governance Standard Operating Procedure (SOP)

**Owner:** PM-007 (Project Manager)  
**Purpose:** How we organize work, name files, and track progress  
**Last Updated:** 2026-01-14  

---

## The Structure (Where Things Live)

```
Epic (E0X_EpicName)
├── epic.md                         ← Epic definition & deliverables
├── summaries/                      ← Summaries + DoD checklist
│   ├── EXECUTIVE_SUMMARY.md
│   ├── DoD.md
│   └── ...
├── deliverables/                   ← D0X.Y_Name folders
│   └── D0X.Y_DeliverableName/
│       ├── deliverable.md          ← What's being delivered
│       ├── requirements/           ← R0X.Y folders
│       │   └── R0X.Y_RequirementName/
│       │       ├── requirement.md  ← Acceptance criteria
│       │       ├── tasks/          ← T0X.Y.Z_*.md files
│       │       └── evidence/       ← Completed task artifacts (co-located; canonical)
│       │           ├── T0X.Y.Z_JD-NNN_Artifact.md
│       │           └── ...
│       └── ...
└── E0X_EXECUTION_TRACKER.md        ← Epic-level progress (what's done, what's next)
```

**One rule:** Task specs live in `requirements/R0X.Y/tasks/`, and their evidence lives in `requirements/R0X.Y/evidence/`. Everything for a requirement is in one place.

**Legacy note:** You may see older evidence layouts elsewhere (e.g., root-level `/evidence/` or deliverable-level `deliverables/<D...>/evidence/<R...>/...`). Do not add new artifacts to legacy locations unless a task spec explicitly requires it.

---

## File Naming Rules (Definitive)

| **What You're Creating** | **Naming Rule** | **Example** | **JD-ID Required?** |
|---|---|---|---|
| Epic definition | `epic.md` | `epic.md` | No |
| Deliverable spec | `deliverable.md` | `deliverable.md` | No |
| Requirement spec | `requirement.md` | `requirement.md` | No |
| Task specification | `T0X.Y.Z_JD-NNN_[Name].md` | `T02.1.1_JD-DATA027_ImportDesign.md` | **YES** |
| Task completion artifact | `T0X.Y.Z_JD-NNN_[Type].md` | `T02.1.1_JD-DATA027_ArchitectureDoc.md` | **YES** |
| Epic tracker | `E0X_EXECUTION_TRACKER.md` | `E02_EXECUTION_TRACKER.md` | No |
| Req tracker | `R0X.Y_EXECUTION_TRACKER.md` | `R02.1_EXECUTION_TRACKER.md` | No |
| Root-level anchor | `[Purpose].md` | `PROJECT_STATUS_DASHBOARD.md` | No |

**JD-ID rule:** If a human (or AI hydrating a role) is executing it, the filename includes their JD-ID. If it's a container or artifact, no JD-ID.

---

## What to Update When

| **Event** | **Where** | **What to Update** |
|---|---|---|
| **Task starts** | Task spec | Add start time: `Start: 2026-01-15T09:00Z` |
| **Task blocked** | `PROJECT_STATUS_DASHBOARD.md` | Add blocker line: `BLOCKER: T0X.Y.Z – [reason]` |
| **Task complete** | Task spec + tracker | Mark ✅, add completion time, link evidence artifact |
| **Evidence ready** | `requirements/R0X.Y/evidence/` | Create artifact: `T0X.Y.Z_JD-NNN_[Type].md` with results |
| **Decision needed** | Chat first, then dashboard | ALWAYS come to sponsor with decision context (options + impact), then update dashboard with outcome |
| **Phase gate triggered** | `PROJECT_STATUS_DASHBOARD.md` | Update status, timestamp, next checkpoint |

**Key: PROJECT_STATUS_DASHBOARD.md is the master tracking document.** Updated whenever task state changes (complete, blocked, decision outcome, phase gate). You check this one place; we don't maintain parallel trackers.

---

## Automation (Governance Guardrails)

**Goal:** Keep governance consistent with minimal manual overhead.

**Run these checks whenever you create/move files or close an epic:**

1. **Governance audit** (structure, naming, duplicates):
	- `scripts/governance_audit.py`
2. **Link integrity** (relative links resolve):
	- Use the same audit script output (it reports missing references by location)

**Rules enforced by automation:**
- One deliverable folder per D0X.Y prefix (no parallel variants like `D02.5_TaggingOrganization`).
- Every requirement has `requirement.md` + `DoD.md`.
- Tasks/evidence files follow `T0X.Y.Z_JD-NNN_[Name].md` naming.
- Empty task/evidence folders are flagged for cleanup.

**Reorg rule:** If you are consolidating folders, **move files**. Do not reauthor content unless required.

---

---

## Getting Help From the Sponsor

**When to escalate to the sponsor (in chat):**

❌ **DO NOT say:** "What should I do next?"  
✅ **DO say:** "I need human-derived input on [specific blocker]. [Description of what's blocking.]"

**If there is no blocker:** You have authority to proceed to the next step in the task sequence. Do not wait for permission.

---

---

## PROJECT_STATUS_DASHBOARD.md (What To Keep Current)

One-page snapshot showing:
- ✅ Which epics are COMPLETE, IN PROGRESS, or QUEUED
- 🔴 Critical path (next 3 dependencies)
- ⚠️ Current blockers (if any)
- �� Decisions waiting for you
- 📅 Next checkpoint (when do we sync?)

**Update:** Whenever task state changes. You can scan it anytime to know where we are.

---

## Task Specification Anatomy

Every task file has this structure:

```markdown
# T0X.Y.Z: [Task Name]

**JD:** JD-NNN (e.g., JD-DATA027)  
**Owner:** [Role Name]  
**Estimated Time:** X hours  
**Status:** 🟢 READY / 🟡 IN PROGRESS / ✅ COMPLETE  

## Objective
[One sentence: what are we building/designing/validating?]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Deliverables
- Output 1 (artifact location)
- Output 2 (artifact location)

## DoD Checklist (Task Complete When)
- [ ] All acceptance criteria met
- [ ] Artifacts created in /evidence/ with correct naming
- [ ] Evidence linked from this task spec
- [ ] (If needed) QA/UAT sign-off obtained

## Blocking/Blocked By
- Blocks: T0X.Y.Z+1 (next task in sequence)
- Blocked by: T0X.Y.Z-1 (prerequisite)

---

## Notes
[Any context, decisions, or coordination notes]
```

When the task is complete, you fill in the evidence links and check DoD boxes. Evidence goes in the same requirement folder.

---

## When Next Context Window Arrives

Next session reads:
1. **This file** (SOP) – 5 minutes
2. **README.md** – Understand the project
3. **PROJECT_STATUS_DASHBOARD.md** – Where are we right now?
4. **E0X_EXECUTION_TRACKER.md** – What task am I picking up next?
5. **Task spec file** – Do the task

That's the onboarding. Everything else is reference.

---

## Don't Do This (Anti-Patterns)

❌ Create files without a home (they get lost)  
❌ Name artifacts differently than the pattern (breaks traceability)  
❌ Skip the DoD checklist (hard to know when task is really done)  
❌ Forget to update dashboard (you lose visibility)  
❌ Create elaborate process docs (keep it simple; let the structure speak)  

---

## Decision Log (Light, Event-Driven)

Keep a simple decision log at `/governance/DECISION_LOG.md`:

**Format:**
```
## Decision: [Title]

**Date:** YYYY-MM-DD  
**Question:** What decision was needed?  
**Options:** Option A, Option B, Option C  
**Chosen:** Option X  
**Rationale:** Why this choice?  
**Impact:** What changes as a result?  
```

No signatures. No approval chains. Just: decision made, move forward.

---

## Summary

- **Folder structure:** Epic → Deliverable → Requirement (with tasks + evidence co-located)
- **Files stay findable** by consistent naming and clear homes
- **Tasks are self-contained** (objective + acceptance criteria + DoD)
- **Evidence lives with requirements** (same folder, easy to navigate)
- **Dashboard is your visibility** (updated when things change)
- **Next context window onboards fast** (5 docs, 15 minutes, ready to work)

That's it. Everything else is noise.
