# Governance Essentials — Simplified for 2-Person Team

**Owner:** PM-007 (AI Developer)  
**Audience:** New context windows (next-me) + user (UAT/decision-maker)  
**Purpose:** Quick reference for how we organize work, name files, and track progress  
**Last Updated:** 2026-01-14  

---

## THE STRUCTURE (Where Things Live)

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
│       │       ├── tasks/          ← T0X.Y.Z_*.md
│       │       └── evidence/       ← Completed task artifacts
│       └── ...
└── evidence/
    ├── E0X_EXECUTION_TRACKER.md    ← Task progress (what's done, what's next)
    └── (task completion artifacts)
```

**One rule:** Task output goes to `/evidence/` with same folder structure as `/requirements/`. Easy to match: R0X.Y_Name maps to /evidence/R0X.Y_Name/ for that requirement's evidence.

---

## FILE NAMING RULES (Definitive)

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

## WHAT TO UPDATE WHEN

| **Event** | **Where** | **What to Update** |
|---|---|---|
| **Task starts** | Task spec | Add start time: `Start: 2026-01-15T09:00Z` |
| **Task blocked** | `PROJECT_STATUS_DASHBOARD.md` | Add blocker line: `BLOCKER: T0X.Y.Z – [reason]` |
| **Task complete** | Task spec + tracker | Mark ✅, add completion time, link evidence artifact |
| **Evidence ready** | `/evidence/R0X.Y/` | Create artifact: `T0X.Y.Z_JD-NNN_[Type].md` with results |
| **Decision needed** | `PROJECT_STATUS_DASHBOARD.md` | Add: `DECISION NEEDED: [Question] – answer by [date]` |
| **Weekly check-in** | `PROJECT_STATUS_DASHBOARD.md` | Update all active task progress; highlight blockers |

**Key:** Dashboard is YOUR visibility into what's happening. Updated whenever something changes, not on a schedule.

---

## PROJECT_STATUS_DASHBOARD.md (What To Keep Current)

One-page snapshot showing:
- ✅ Which epics are COMPLETE, IN PROGRESS, or QUEUED
- 🔴 Critical path (next 3 dependencies)
- ⚠️ Current blockers (if any)
- 📌 Decisions waiting for you
- 📅 Next checkpoint (when do we sync?)

**Update:** Whenever task state changes. You can scan it anytime to know where we are.

---

## TASK SPECIFICATION ANATOMY

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

## Evidence Links
- [Artifact 1](../../evidence/R0X.Y/T0X.Y.Z_JD-NNN_Report.md)
- [Artifact 2](../../evidence/R0X.Y/T0X.Y.Z_JD-NNN_Code.md)

## Blocking/Blocked By
- Blocks: T0X.Y.Z+1 (next task in sequence)
- Blocked by: T0X.Y.Z-1 (prerequisite)

---

## Notes
[Any context, decisions, or coordination notes]
```

When the task is complete, you fill in the evidence links and check DoD boxes. That's it.

---

## WHEN NEXT-ME ARRIVES (Context Window Resets)

Next-me reads:
1. **This file** (Governance_SIMPLIFIED.md) – 5 minutes
2. **README.md** – Understand the project
3. **PROJECT_STATUS_DASHBOARD.md** – Where are we right now?
4. **E0X_EXECUTION_TRACKER.md** – What task am I picking up next?
5. **Task spec file** – Do the task

That's the onboarding. Everything else is reference.

---

## DON'T DO THIS (Anti-Patterns)

❌ Create files without a home (they get lost)  
❌ Name artifacts differently than the pattern (breaks traceability)  
❌ Skip the DoD checklist (hard to know when task is really done)  
❌ Forget to update dashboard (you lose visibility)  
❌ Create elaborate process docs (keep it simple; let the structure speak)  

---

## DECISION LOG (Light, Event-Driven)

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

## SUMMARY

- **Folder structure:** Epic → Deliverable → Requirement → Task → Evidence
- **Files stay findable** by consistent naming and clear homes
- **Tasks are self-contained** (objective + acceptance criteria + DoD)
- **Dashboard is your visibility** (updated when things change)
- **Evidence maps to requirements** (requirement.md → evidence/ artifacts)
- **Next-me onboards fast** (5 docs, 15 minutes, ready to work)

That's it. Everything else is noise.
