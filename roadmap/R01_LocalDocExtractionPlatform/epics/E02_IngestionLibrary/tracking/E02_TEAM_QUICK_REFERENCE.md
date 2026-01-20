# E02 QUICK REFERENCE CARD – TEAM EXECUTION GUIDE

**Updated:** 2026-01-14T22:00Z  
**For:** All E02 team members (9 people)  
**Purpose:** Quick answers to common questions during E02 execution phase

---

## WHAT'S HAPPENING RIGHT NOW?

**E01 Status:** 99% complete (1 validation pending, ~24 hours)  
**E02 Status:** Specs complete ✅ | Execution planning complete ✅ | Ready to kickoff 2026-01-15  
**Your Role:** Assigned to E02 task execution starting 2026-01-15 (pending approvals)

---

## STATE-BASED EXECUTION (NO CALENDAR CEREMONIES)

**How E02 Works:**
- Tasks progress through states: QUEUED → READY → STARTED → (BLOCKED) → COMPLETE
- **No daily standups.** Status updates happen in E02_EXECUTION_TRACKER.md automatically when task states change.
- **No weekly checkpoints.** Phase gates trigger automatically when all Phase N tasks complete + QC-101 signs off.
- **No RAID review meetings.** Risks are monitored continuously. When a threshold crosses, PM-007 is alerted immediately.
- **No calendar-based anything.** Phases start when prerequisites complete, not on specific dates.

**Your Obligations:**
1. **Update Task State** when you move work (QUEUED → STARTED, encounter BLOCKED, etc.)
2. **Report Blockers Immediately** (don't wait for standup) – message PM-007 or DEV-024 within 1 hour
3. **Get QC-101 Sign-Off** when your task meets Definition of Done

**Timeline Expectations:**
- Phase 1 expected ~3 days (but gates on completion, not calendar)
- Phase 2 expected ~8 days (but gates on completion, not calendar)
- Phase 3 expected ~8 days (but gates on completion, not calendar)
- If tasks finish early, phases start early. If blocked, timeline adjusts.

---

## CRITICAL DATES (BLOCKING EVENTS, NOT CEREMONIES)

| Date | Event | Why It Matters |
|------|-------|----------------|
| **2026-01-15 EOD** | E01 validation + availability decisions | If E01 passes + DEV-033/034 confirmed, Phase 1 can start |
| **When all Phase 1 tasks COMPLETE** | Phase 1 → Phase 2 auto-transition | No "Friday checkpoint" – just state change |
| **When blocker >4 hours old** | Auto-escalation to PM-007 | Don't hide blockers; they escalate automatically |
| **When Phase 2 all tasks COMPLETE** | Phase 2 → Phase 3 auto-transition | Again, state-based, not calendar |
| **2026-02-04 (Target)** | E02 Exit Gate | All 16 tasks complete + DoD verified. Target only; gates on completion |

**NO STANDUPS. NO CHECKPOINTS. STATUS IS REAL-TIME IN E02_EXECUTION_TRACKER.MD.**

---

## YOUR TASK ASSIGNMENT

Find your name below. That's your task for E02:

| Name | Task ID | Task Name | Estimated Hours | Start Date | Deliverable |
|------|---------|-----------|-----------------|-----------|-------------|
| **DEV-024** | T02.1.3, T02.5.1 | Batch import + tagging schema | 40-60 + 4 | 2026-01-15 | D02.1, D02.5 |
| **DEV-003** | T02.2.2, T02.2.3 | Hash algorithm + dedup impl | 5 + 8 | 2026-01-15 | D02.2 |
| **DEV-033** | T02.3.3 | Performance optimization | 8 | *Pending* | D02.3 |
| **DEV-034** | T02.3.2 | Schema migrations | 6 | *Pending* | D02.3 |
| **DATA-024** | T02.4.1, T02.4.2 | Classification taxonomy + impl | 6 + 12 | 2026-01-15 | D02.4 |
| **QC-101** | T02.1.4, T02.2.4, T02.4.3, T02.5.2 | All phase validations | 6+6+8+4 | *Phase 3* | All |
| **AGENT-002** | Support | E02 support (10%) + E03 prep | — | Ongoing | N/A |

*"Pending" = awaiting availability confirmation due 2026-01-15 EOD*

---

## WHERE TO FIND EVERYTHING

**Your Task Spec:**
- Location: `/Reserved/DocExtractor/roadmap/R01_LocalDocExtractionPlatform/epics/E02_IngestionLibrary/tasks/`
- File: `T0X.Y.Z_JD-XXX_YourTaskName.md`
- Contains: Acceptance criteria, DoD checklist, embedded JD context, dependencies

**Execution Plan:**
- [E02_DELIVERY_EXECUTION_PLAN.md](../evidence/E02_DELIVERY_EXECUTION_PLAN.md) – 3-phase timeline, critical path, your capacity

**What Not to Miss:**
- [E02_KICKOFF_CHECKLIST.md](../evidence/E02_KICKOFF_CHECKLIST.md) – Pre-execution readiness (who must confirm what by when)
- [E02_DECISION_LOG.md](../evidence/E02_DECISION_LOG.md) – Decisions made + decisions pending
- [PROJECT_STATUS_DASHBOARD.md](../PROJECT_STATUS_DASHBOARD.md) – Real-time epic status

---

## YOUR EXECUTION RESPONSIBILITIES (NO CEREMONIES, STATE-BASED ONLY)

### What You Must Do

1. **Update Your Task State** when it changes
   - Start work? Update task state to STARTED in tracker
   - Hit a blocker? Update to BLOCKED (don't wait for standup)
   - Complete work with evidence? Mark COMPLETE, tag QC-101, request sign-off

2. **Report Blockers Immediately** (not at standup)
   - Message PM-007 or DEV-024 within 1 hour of being blocked
   - Include: what's blocked, why, when you expect to unblock, what you need from others
   - If blocked >4 hours, system auto-escalates to PM-007

3. **Get QC-101 Sign-Off** when task meets Definition of Done
   - Don't mark task done without QC approval
   - QC-101 validates against acceptance criteria in your task spec
   - No testing phase without QC on record

4. **Check E02_EXECUTION_TRACKER.md** for real-time status
   - No need to wait for standup to know phase status
   - Your task state changes appear immediately
   - Blocker escalations appear immediately

### What You DON'T Do

- ❌ Attend daily standups (no standups; status is async)
- ❌ Wait for weekly checkpoints to report progress (report immediately)
- ❌ Discuss risks at Monday RAID review meeting (risks escalate automatically when threshold crossed)
- ❌ Batch updates for end-of-week (update state immediately)

**If you're blocked, stuck, or have a question: Tell PM-007 or DEV-024 right now. Don't wait.**

---

## CRITICAL SUCCESS FACTORS (WATCH THESE)

### 🔴 CRITICAL PATH: D02.2 Deduplication (18 hours)
**Why?** It's the bottleneck. If D02.2 slips, entire E02 slips proportionally.  
**Who?** DEV-003 owns this (T02.2.2 hash + T02.2.3 dedup impl).  
**Your Job:** If you're DEV-003, protect this at all costs. If you depend on DEV-003, plan for it. If blocked >1 hour, escalate immediately.

### 🟡 LONGEST TASK: T02.1.3 Import (40-60 hours)
**Why?** Highest risk task; biggest time sink.  
**Who?** DEV-024 owns this.  
**Your Job:** If you're DEV-024, monitor weekly. If you depend on DEV-024, know they're busy.

### 🟡 QUALIFICATION RISK: QC-101 Availability
**Why?** QC-101 is the only QA resource. If they can't run 3 test phases concurrently, Phase 3 extends 9 days.  
**Who?** PM-007 & DEV-024 tracking this (DECN-E02-WAIT-002 pending).  
**Your Job:** Wait for go-ahead on parallel vs sequential testing.

---

## DEFINITION OF DONE (DOD) – YOUR TASK COMPLETE WHEN:

- ✅ **Acceptance Criteria Met:** All criteria in your task spec verified
- ✅ **Tests Passing:** Your code has tests; 80%+ coverage required
- ✅ **Evidence Collected:** Logs, screenshots, test results archived in `evidence/`
- ✅ **Docs Updated:** README, architecture, onboarding updated if needed
- ✅ **QC-101 Sign-Off:** Your task owner (QC-101 or designated lead) approves

**No task is done until ALL of these are true.** Partial work doesn't count.

---

## WHAT TO DO WHEN YOU'RE BLOCKED

1. **Identify the blocker:** What's preventing you from making progress?
2. **Check the delivery plan:** Is it a known dependency? See [E02_DELIVERY_EXECUTION_PLAN.md](../evidence/E02_DELIVERY_EXECUTION_PLAN.md)
3. **Report immediately:** Don't wait until standup. Message DEV-024 or PM-007 within 1 hour.
4. **Provide context:** "Task [ID], blocker is [X], depends on [Y], impacts [Z]"
5. **Propose solution:** "I can [do this] as workaround" or "Need [resource] from [person] by [time]"

---

## WHAT IF YOUR TASK ASSIGNMENT CHANGES?

**Watch for:**
- DEV-033 & DEV-034 pending approval (due 2026-01-15 EOD)
- If they're NOT approved, their tasks get reassigned to DEV-003 (Phase 2 gets longer)
- If they ARE approved, your timeline stays on track

---

## ACRONYMS & TERMINOLOGY

| Term | Meaning | Why You Care |
|------|---------|-------------|
| **DoD** | Definition of Done | Your task must satisfy all DoD criteria to be marked complete |
| **QC** | Quality Control | QC-101 validates your work; can't proceed without sign-off |
| **RAID** | Risks, Assumptions, Issues, Dependencies | Tracked weekly at Monday 10am meeting |
| **E01, E02, etc** | Epic 1, Epic 2, etc | E02 is your current work; E03 depends on E02 exit gate |
| **D02.1, D02.2, etc** | Deliverable 2.1, 2.2, etc | Your tasks roll up to one of these 5 deliverables |
| **T02.1.3** | Task 2.1.3 | Your specific task ID; see your task spec for details |
| **JD-XXX** | Job Description ID | Your role; embedded in task specs for context |

---

## COMMON QUESTIONS

**Q: When does E02 actually start?**  
A: 2026-01-15, assuming E01 validation passes and 2 pending decisions resolve by EOD. Otherwise, 2026-01-16 or later.

**Q: What if I don't know how to do my task?**  
A: 1) Read your task spec (has acceptance criteria + context). 2) Check evidence artifacts from similar prior work. 3) Ask DEV-024 in standup.

**Q: What if I finish early?**  
A: Grab your next task from the roadmap (ask DEV-024). Don't sit idle; keep the critical path moving.

**Q: What if I finish late?**  
A: Report blockers immediately. Don't hide delays. We adjust the plan if needed, but we need to know ASAP.

**Q: Who do I ask if my task spec is wrong?**  
A: Your task spec author (JD-ID in filename). If still confused, escalate to DEV-024.

**Q: What if I find a bug in someone else's code?**  
A: Document it. Report to DEV-024. They'll assign it as a blocker or fix.

---

## CONTACT MATRIX

| Need | Contact | Channel | Response Time |
|------|---------|---------|----------------|
| **Daily Standup** | DEV-024 | Slack/Teams | 9:00 AM daily |
| **Blocker/Help** | DEV-024 | Slack/Teams | <1 hour during work hours |
| **Decision/Escalation** | PM-007 | Slack/Teams + Email | <2 hours |
| **QA Sign-Off** | QC-101 | Slack/Teams | <1 day (depends on queue) |
| **Technical Question** | Your Task Spec Author | Slack/Teams | <2 hours |

---

## FINAL REMINDERS

1. **Check your email/Slack** before standup each day (task updates, schedule changes)
2. **Read your task spec** – it has everything you need
3. **Report blockers early** – don't wait until they blow up
4. **Keep code modular** – the architecture emphasizes clear separation of concerns
5. **Test as you go** – don't wait until end to write tests
6. **Archive evidence** – screenshots, logs, test results go in `evidence/`
7. **Don't skip DoD** – all criteria must pass before marking done

---

**Questions?** Message PM-007 or DEV-024  
**Status Dashboard:** [PROJECT_STATUS_DASHBOARD.md](../PROJECT_STATUS_DASHBOARD.md)  
**Full Execution Plan:** [E02_DELIVERY_EXECUTION_PLAN.md](../evidence/E02_DELIVERY_EXECUTION_PLAN.md)

**Last Updated:** 2026-01-14T22:00Z  
**Owner:** PM-007

