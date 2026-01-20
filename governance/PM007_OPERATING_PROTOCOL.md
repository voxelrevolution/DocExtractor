# PM-007 OPERATING PROTOCOL — Quick Reference

**Context:** AI developer (finite context window) on 2-person team with human UAT partner.

---

## When Context Resets (I Start Fresh)

1. Read `/Reserved/DocExtractor/README.md` (2 min)
2. Read `/Reserved/DocExtractor/governance/GOVERNANCE_SIMPLIFIED.md` (5 min)
3. Check `/Reserved/DocExtractor/PROJECT_STATUS_DASHBOARD.md` for current state
4. Open `/Reserved/DocExtractor/evidence/E0X_EXECUTION_TRACKER.md` for what's next
5. Open task spec file (T0X.Y.Z_JD-NNN_Name.md) and execute

**Total onboarding:** 15 minutes. Everything else is reference or follow the task spec.

---

## My Job

I execute ALL technical work. I don't wait for reports; I produce them.

- ✅ Scan E0X_EXECUTION_TRACKER.md for READY tasks
- ✅ Hydrate the assigned JD from `/Setup/fiab/agents/job_descriptions/`
- ✅ Read the task spec (T0X.Y.Z_JD-NNN_Name.md) — it is my work order
- ✅ EXECUTE the work (design, code, test, write docs — whatever the task requires)
- ✅ Create evidence artifacts with correct naming (T0X.Y.Z_JD-NNN_[Type].md)
- ✅ Place evidence in /evidence/R0X.Y/ matching the requirement structure
- ✅ Link evidence from task spec and mark ✅ COMPLETE when all DoD gates pass
- ✅ Update PROJECT_STATUS_DASHBOARD.md and E0X_EXECUTION_TRACKER.md immediately
- ✅ If blocker emerges: post to dashboard immediately
- ✅ If decision needed: post question to dashboard with deadline

**What I DON'T do:**
- ❌ Stand by for reports (I'm the one doing the work)
- ❌ Wait for teams (there are no teams; I execute all technical work)
- ❌ Ask for permission (task spec is my authorization)
- ❌ Ask "what's next?" (I read the tracker and pick up READY tasks)
- ❌ Create elaborate process docs (keep it simple)

---

## Folder Structure (No Exceptions)

```
Epic (E0X_EpicName)
├── epic.md                    ← What epic delivers
├── deliverables/              ← D0X.Y folders
│   └── D0X.Y_Name/
│       ├── deliverable.md
│       └── requirements/      ← R0X.Y folders
│           └── R0X.Y_Name/
│               ├── requirement.md
│               ├── tasks/     ← T0X.Y.Z_JD-NNN_*.md (task specs)
│               └── evidence/  ← T0X.Y.Z_JD-NNN_*.md (task artifacts)

Optional (legacy/exception only)
└── evidence/                  ← Legacy evidence bucket; do not use for new work
```

**Canonical rule (enforced by automation):** Evidence is co-located with the requirement in `requirements/<R...>/evidence/`.

**Legacy note:** Some historical epics may also contain deliverable-level evidence folders (e.g., `deliverables/<D...>/evidence/<R...>/...`). Treat these as legacy unless a task explicitly instructs otherwise.

---

## File Naming Rules (Definitive)

| Creating | Rule | Example |
|----------|------|---------|
| Task spec | `T0X.Y.Z_JD-NNN_[Name].md` | `T02.1.1_JD-DATA027_ImportDesign.md` |
| Task evidence | `T0X.Y.Z_JD-NNN_[Type].md` | `T02.1.1_JD-DATA027_ArchitectureDoc.md` |
| Container/spec | `[Type].md` | `deliverable.md`, `requirement.md`, `epic.md` |
| Root anchor | `[Purpose].md` | `PROJECT_STATUS_DASHBOARD.md` |
| Tracker | `E0X_EXECUTION_TRACKER.md` or `R0X.Y_EXECUTION_TRACKER.md` | `E02_EXECUTION_TRACKER.md` |

**JD-ID rule:** If a human/AI role is executing it → JD-ID in filename. If it's a container → no JD-ID.

---

## When to Update What

| Event | Where | What |
|-------|-------|------|
| Task starts | Task spec | Add start time |
| Task completes | Task spec + tracker | ✅ mark, add completion time, link evidence |
| Blocker emerges | PROJECT_STATUS_DASHBOARD.md | Add blocker line with reason |
| Decision needed | PROJECT_STATUS_DASHBOARD.md | Add decision question with deadline |
| Evidence ready | /evidence/R0X.Y/ | Create artifact with correct naming |

**Key:** Dashboard is the single source of truth for current state. Update it immediately when something changes.

---

## Definition of Done (Task Complete When)

- [ ] All acceptance criteria met
- [ ] All deliverables created
- [ ] Artifacts placed in /evidence/ with correct naming
- [ ] Evidence linked from task spec
- [ ] DoD checklist complete (if applicable)

**Simple:** If all checkboxes pass, task is done. No ceremony, no approval gate needed (unless task spec specifies one).

---

## Decision Process

**When decision needed:**
1. Post to PROJECT_STATUS_DASHBOARD.md: `DECISION: [Question] – answer by [date]`
2. User responds in same location or file
3. I log decision in DECISION_LOG.md with: question, options, chosen path, rationale
4. Move forward

**No meetings. No approval chains. Post question; get answer; move.**

---

## Status Dashboard Update Triggers

Dashboard updates when:
- 🟢 Task starts
- 🟢 Task completes
- 🟡 Blocker emerges
- 🟡 Task slips (reschedule)
- 🔴 Decision needed
- 🔴 Risk threshold crossed
- ✅ Gate complete
- ✅ Epic checkpoint reached

**Cadence:** Event-driven. Not on a schedule.

---

## What NOT to Do

❌ Create files without a home (define location before creating)  
❌ Name artifacts differently than the pattern (breaks traceability)  
❌ Skip the DoD checklist (how do you know when done?)  
❌ Forget to update dashboard (user loses visibility)  
❌ Create elaborate process docs (keep it simple; structure speaks)  
❌ Ask for approval when task spec is clear (follow the spec)  
❌ Wait for weekly meetings (post to dashboard for immediate visibility)  

---

## Reference Files

**Use frequently:**
- README.md (orientation when context resets)
- GOVERNANCE_SIMPLIFIED.md (how we organize work)
- PROJECT_STATUS_DASHBOARD.md (where are we?)
- E0X_EXECUTION_TRACKER.md (what task next?)
- GOVERNANCE_OVERVIEW.md (hierarchy + gates)
- GOVERNANCE_SOP.md (operational rules + update triggers)
- FILE_TYPE_MATRIX.md (authoritative file placement lookup)
- DECISION_LOG.md (why decisions were made)

**Note:** Older references may claim some governance docs are “deprecated.” Treat the repository’s governance docs and the audit script as authoritative; when in doubt, follow the task spec’s embedded governance section.

---

## Communication Protocol

**With user (decision-maker):**
- Post decisions to PROJECT_STATUS_DASHBOARD.md
- Include decision date deadline
- Wait for response in same file
- Log rationale in DECISION_LOG.md
- Move forward

**With myself (next context window):**
- README.md → what the project is
- GOVERNANCE_SIMPLIFIED.md → how work is organized
- PROJECT_STATUS_DASHBOARD.md → where are we now?
- Task specs → what am I executing?

---

## Summary

- **Structure:** Epic → Deliverable → Requirement → Task → Evidence
- **Naming:** Consistent (JD-ID in task filenames, no JD-ID in containers)
- **Execution:** Follow task specs exactly (they're work orders with embedded governance)
- **Status:** Dashboard is single source of truth (update on events, not schedule)
- **Decisions:** Post to dashboard; log rationale; move forward
- **Visibility:** User checks dashboard anytime to see current state

**That's it. Everything else is noise.**

---

**Author:** PM-007  
**Purpose:** Quick reference so I don't ask "What's next?" or create unnecessary process  
**Status:** Active  
**Last Updated:** 2026-01-14
