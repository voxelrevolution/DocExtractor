# DECISION LOG

**Owner:** PM-007 (Project Manager)  
**Purpose:** Track all significant decisions with context, options, chosen path, rationale, and impact  
**Last Updated:** 2026-01-13  
**Access:** Reference for understanding why choices were made; prevents rehashing old decisions  

---

## DECISION: PROJECT_STATUS_DASHBOARD.md — ROOT-LEVEL GOVERNANCE ANCHOR

**Decision ID:** DEC-001-ProjectStatusDashboard  
**Date:** 2026-01-13  
**Decision Maker:** PM-007  
**Status:** APPROVED (Effective immediately)  
**Impact:** Project-wide governance enforcement  

---

### Situation

E02 kickoff revealed critical file organization violations:
- E02 missing required subdirectories (/deliverables/, /requirements/, /tasks/)
- Epic summary docs scattered at project root (E02_KICKOFF_READY.md, E02_KICKOFF_SUMMARY.md)
- Evidence artifacts lacked JD-ID owner designation
- No governance enforcement mechanism existed

User halted work and demanded comprehensive governance assessment and prevention system.

**Key Question:** Is PROJECT_STATUS_DASHBOARD.md a governance anchor (root-level, permanent) or an artifact (should be versioned with epics)?

---

### Options Considered

| Option | Pros | Cons | Recommendation |
|--------|------|------|-----------------|
| **A: Governance Anchor (Root-Level)** | Always visible; high-level health snapshot; stakeholder-friendly; clear escalation path | Requires discipline to keep current; single point of failure if not updated; not tied to epic lifecycle | ✅ **CHOSEN** |
| **B: Epic Artifact (Versioned per Epic)** | Clear ownership per epic; versioned with epic evidence; part of artifact trail | Scattered across epics; hard to get project-wide health at root; requires aggregation; users don't know where to look | ❌ Rejected |
| **C: Hybrid (Root + Epic-Versioned)** | Best of both options; executive view at root + detailed per epic | Requires maintenance discipline; duplicate tracking; increases complexity | ⚠️ Considered but rejected as over-engineering |

---

### Decision: GOVERNANCE ANCHOR (Option A)

**PROJECT_STATUS_DASHBOARD.md stays at project root** and serves as the single source of truth for project-wide health.

### Governance Status

- **Location:** `/Reserved/DocExtractor/PROJECT_STATUS_DASHBOARD.md` (root-level, permanent)
- **Owner:** PM-007 (non-delegable)
- **Purpose:** Executive stakeholder alignment on project health (not artifact storage)
- **Audience:** Sponsor, leadership, cross-functional stakeholders
- **Update Cadence:** Every Friday EOD + event-driven on epic completion
- **Refresh Cycle:** Weekly minimum (non-negotiable)

### Content Model (Lightweight, Actionable)

Minimum content per update:

```
PROJECT STATUS DASHBOARD
═══════════════════════════════════════════════════════════════

EPIC STATUS (RAG Summary)
├─ E01: ████████████████████ 100% COMPLETE ✅
├─ E02: ████░░░░░░░░░░░░░░░ 25% In Progress 🟡
├─ E03: ░░░░░░░░░░░░░░░░░░░░  0% Upcoming (not started)
├─ E04: ░░░░░░░░░░░░░░░░░░░░  0% Upcoming (not started)
└─ E05: ░░░░░░░░░░░░░░░░░░░░  0% Upcoming (not started)

CRITICAL PATH (Next 3 Weeks)
├─ Week 1 (Jan 13-19): E02 D02.1 scoping complete (PM-001)
├─ Week 2 (Jan 20-26): E02 D02.2, D02.3 database schema (DEV-003)
└─ Week 3 (Jan 27-Feb 2): E02 D02.4 prompt engineering (AGENT-002)

TOP 3 ACTIVE RISKS
├─ [RISK-001] External dependency on [System] delays D02.2 (MEDIUM, owner: DEV-003)
├─ [RISK-002] Prompt quality validation not ready for D02.4 (LOW, owner: AGENT-002)
└─ [RISK-003] Test coverage for D02.5 unclear (MEDIUM, owner: QC-101)

DECISIONS NEEDED
├─ Approve E02 scope (sponsor decision by Jan 17)
├─ Approve infrastructure approach for D02.3 (arch decision by Jan 20)
└─ Approve post-MVP feature deferral (PM/PO decision by Jan 25)

LINKS TO DETAILED STATUS
├─ RAID Log: /governance/RAID_LOG.md
├─ Decision Log: /governance/DECISION_LOG.md
├─ E02 Status: /roadmap/.../epics/E02_IngestionLibrary/evidence/E02_EXECUTION_TRACKER.md
└─ Previous Dashboards: /archive/PROJECT_STATUS_DASHBOARD_[date].md

NEXT CHECKPOINT
└─ Friday 2026-01-17 EOD (Weekly refresh)
```

### Rationale

1. **Stakeholder Accountability:** Executives expect project health at the top level, not buried in epic hierarchy
2. **Escalation Path:** Red flags on dashboard → drive to RAID log → drive escalation and decisions
3. **Governance Anchor:** Clear signal of what's healthy/at-risk/blocked across all epics
4. **Single Source of Truth:** Prevents confusion from multiple status reports
5. **Prevents Drift:** Hard-to-find status docs delay decisions and create surprises

### Enforcement

- **Weekly Update:** PM-007 updates every Friday 5 PM
- **Milestone Update:** Within 24 hours of epic completion
- **Audit:** Weekly validation (part of GOVERNANCE_SOP.md)
- **Escalation:** Red status automatically triggers RAID log action

### Traceability

- Linked from: [NAVIGATION_GUIDE.md](/NAVIGATION_GUIDE.md), [INDEX.md](/INDEX.md)
- References: [RAID_LOG.md](/governance/RAID_LOG.md), [DECISION_LOG.md](/governance/DECISION_LOG.md), epic evidence trackers
- Updated by: PM-007 (enforced)

---

## DECISION: GOVERNANCE FRAMEWORK — FILE PLACEMENT STANDARD

**Decision ID:** DEC-002-FileOrganizationGovernance  
**Date:** 2026-01-13  
**Decision Maker:** PM-007  
**Status:** APPROVED (Binding, effective immediately)  
**Impact:** All future file creation must comply; E02 execution blocked until corrections applied  

---

### Situation

Analysis revealed that governance violations occurred not because of negligence, but because:

1. ❌ **No file placement checklist existed** — team couldn't validate before creating files
2. ❌ **No file type matrix existed** — ambiguity on where things belong
3. ❌ **No escalation path existed** — team had no way to ask "where does this go?"
4. ❌ **No enforcement mechanism existed** — violations went undetected until end of E02 design

User demanded: "Update your instructional guidance docs to prevent this from happening again."

---

### Decision: COMPREHENSIVE GOVERNANCE FRAMEWORK

Establish three new governance documents:

1. **FILE_PLACEMENT_CHECKLIST.md** — 10-point pre-commit validation required before ANY file creation
2. **FILE_TYPE_MATRIX.md** — Exhaustive mapping of file type → home location → naming convention
3. **GOVERNANCE_SOP.md** — Standard Operating Procedure for enforcement, escalation, and continuous validation

### What Each Document Enforces

**FILE_PLACEMENT_CHECKLIST.md:**
- ✅ Purpose: Every file must have a single-sentence rationale (if not, don't create it)
- ✅ Home: Location defined in FILE_TYPE_MATRIX.md (if ambiguous, escalate)
- ✅ Naming: Convention matches file type (JD-ID required/prohibited per type)
- ✅ Owner: Named person responsible for maintenance (clear accountability)
- ✅ Refresh: Realistic update frequency documented
- ✅ Reference: At least one searchable link from another doc
- ✅ Searchability: Findable via INDEX or NAVIGATION
- ✅ Lifecycle: Archive/delete plan understood
- ✅ No Duplication: Similar files checked before creation
- ✅ JD-ID Compliance: Correct inclusion/exclusion per file type

**FILE_TYPE_MATRIX.md:**
- Exhaustive lookup table: File Type → Location → Naming Convention → JD-ID Rule → Owner → Refresh Cycle
- Decision tree: "What type am I creating?" → Find its home and naming
- Quick reference: 50+ file types from governance anchors to code to evidence artifacts
- Validation: Cross-referenced with GOVERNANCE_OVERVIEW.md hierarchy

**GOVERNANCE_SOP.md:**
- Pre-commit validation workflow for each role (task creator, epic lead, evidence collector, PM)
- Escalation matrix: Issue severity → escalation path → SLA → PM-007 decision
- Weekly validation audit (PM-007 runs Friday EOD)
- Monthly governance review (first Monday of month)
- Root cause prevention: What went wrong in E02 and how to prevent recurrence

### Naming Rules (Definitive)

| File Type | JD-ID Required? | Pattern | Example |
|-----------|-----------------|---------|---------|
| Task specification | **YES** | T0X.Y.Z_JD-NNN_[Name].md | T02.1.1_PM-001_ScopeIngestLibrary.md |
| Task evidence | **YES** (should) | T0X.Y.Z_JD-NNN_[Type].md | T02.1.1_PM-001_ValidationReport.md |
| Epic summary | **NO** | [Type].md | EXECUTIVE_SUMMARY.md, DoD.md |
| Epic folder | **NO** | epic.md | epic.md |
| Root-level file | **NO** | [Name].md | PROJECT_STATUS_DASHBOARD.md |
| Deliverable spec | **NO** | deliverable.md | deliverable.md |
| Requirement spec | **NO** | requirement.md | requirement.md |

### Enforcement Mechanism

**Before File Creation:**
1. Creator runs FILE_PLACEMENT_CHECKLIST.md (10-point validation)
2. If ANY checkbox fails → Stop and escalate to PM-007
3. PM-007 provides guidance within 24 hours
4. File created only AFTER all checkboxes pass

**Weekly Validation (PM-007):**
1. Friday EOD audit of all new files created that week
2. Verify: location correct, naming compliant, linked from parent, searchable, lifecycle clear
3. If violations found → Move files immediately or get approval for exceptions
4. Report status in PROJECT_STATUS_DASHBOARD.md

**Monthly Governance Review (PM-007):**
1. Review DECISION_LOG and RAID_LOG for completeness
2. Audit FILE_TYPE_MATRIX.md for new file types
3. Review governance docs for coherence and sync
4. Report findings to sponsor

### Root Cause Prevention

**Why E02 Violations Occurred:**
- Pre-commit validation checklist didn't exist → files created without verification
- FILE_TYPE_MATRIX didn't exist → ambiguity on home locations
- No escalation path → team couldn't ask PM-007 for guidance
- No weekly audit → violations went undetected

**Corrective Actions (Now in Place):**
- ✅ FILE_PLACEMENT_CHECKLIST.md created — non-negotiable pre-commit validation
- ✅ FILE_TYPE_MATRIX.md created — exhaustive reference with zero ambiguity
- ✅ GOVERNANCE_SOP.md created — clear workflows, escalation paths, enforcement
- ✅ Weekly audit enforced — PM-007 validates every Friday EOD
- ✅ Monthly review enforced — governance health tracked continuously

### Scope of Applicability

**Applies to:**
- ✅ All task specifications (T0X.Y.Z files)
- ✅ All epic-level documents
- ✅ All evidence artifacts
- ✅ All governance documents
- ✅ All execution trackers
- ✅ Any file created in roadmap/, governance/, evidence/, docs/ directories

**Does NOT Apply to:**
- ❌ Code files (src/, tests/) — use code review process
- ❌ Generated artifacts (build outputs, logs) — excluded from governance
- ❌ Configuration files (pyproject.toml, etc.) — governed by code review

---

## DECISION: EPIC FOLDER TEMPLATE & MANDATORY STRUCTURE

**Decision ID:** DEC-003-EpicFolderTemplate  
**Date:** 2026-01-13  
**Decision Maker:** PM-007  
**Status:** APPROVED (Mandatory for all epics)  
**Impact:** Every epic must have identical directory structure  

---

### Decision

Every epic must be created with this exact directory structure:

```bash
mkdir -p /roadmap/R01_LocalDocExtractionPlatform/epics/ExX_EpicName/{summaries,deliverables,requirements,tasks}
```

**No Epic Is Complete Until All Folders Exist.**

### Why

- **Consistency:** Every epic has identical structure (predictable navigation)
- **Completeness:** Prevents incomplete epics missing subdirectories
- **Enforcement:** Pre-commit checklist verifies all folders exist before epic kickoff approved

### Validation

**Before Epic Kickoff Approval:**
- [ ] Epic folder exists with correct name (ExX_EpicName)
- [ ] /summaries/ folder created and populated
- [ ] /deliverables/ folder created (ready for D0X.Y specs)
- [ ] /requirements/ folder created (ready for R0X.Y specs)
- [ ] /tasks/ folder created (ready for T0X.Y.Z files)
- [ ] epic.md file created in root
- [ ] All summaries linked from epic.md
- [ ] All docs added to INDEX.md and NAVIGATION_GUIDE.md

If ANY folder is missing → Epic kickoff BLOCKED until structure is complete.

---

## DECISION: PM-007 GOVERNANCE AUTHORITY

**Decision ID:** DEC-004-PMGovernanceAuthority  
**Date:** 2026-01-13  
**Decision Maker:** PM-007  
**Status:** APPROVED (Non-delegable authority)  
**Impact:** Final arbitration on all governance questions  

---

### Decision

PM-007 is the ultimate authority on:

1. **File Placement:** Where any file belongs (escalation authority)
2. **Naming Conventions:** Whether a filename complies (enforcement authority)
3. **Governance Framework:** Updates to FILE_TYPE_MATRIX.md, FILE_PLACEMENT_CHECKLIST.md, GOVERNANCE_SOP.md
4. **Escalation Resolution:** Final decision on governance questions (24-hour SLA)
5. **Violation Correction:** Authority to move files, rename files, update structure
6. **Weekly Validation:** Authority to enforce audit findings immediately
7. **Decision Log:** Authority to document decisions binding on all team members

### Authority & Responsibility

- **Authority:** Final decision on governance disputes (binding, non-appealable)
- **Responsibility:** Maintain governance documentation; run audits; keep framework in sync with actual structure
- **Non-Delegable:** Escalation resolution, governance updates, and enforcement cannot be delegated

### Escalation Path

**Team Member:** "I don't know where to put this file."
→ **PM-007:** "Use FILE_TYPE_MATRIX.md. If not found, send me the details and I'll respond in 24 hours."
→ **Outcome:** File created (if approved) + FILE_TYPE_MATRIX.md updated (if new file type)

---

## ONGOING DECISIONS (TO BE MADE)

| Decision | Status | Impact | Owner | Timeline |
|----------|--------|--------|-------|----------|
| Archive directory structure (where do old epics live?) | ⏳ PENDING | How to retire completed epics | PM-007 | Before E02 completion |
| Meeting notes organization | ⏳ PENDING | Where do sync notes live? Linked from sprint? | PM-007 | Before first sprint planning |
| Code review vs. governance audit separation | ⏳ PENDING | Code files exempt from FILE_PLACEMENT_CHECKLIST? | PM-007 + DEV-024 | Next sprint |
| JD-ID suffix on all evidence files (optional vs. required) | ⏳ PENDING | Should ALL evidence include JD-ID or just task-level? | PM-007 | Before next evidence artifact |

---

## VERSION HISTORY

| Date | Version | Decision | Status | Owner |
|------|---------|----------|--------|-------|
| 2026-01-13 | 1.0 | DEC-001: PROJECT_STATUS_DASHBOARD as governance anchor | APPROVED | PM-007 |
| 2026-01-13 | 1.0 | DEC-002: Comprehensive file organization governance | APPROVED | PM-007 |
| 2026-01-13 | 1.0 | DEC-003: Epic folder template mandatory | APPROVED | PM-007 |
| 2026-01-13 | 1.0 | DEC-004: PM-007 governance authority | APPROVED | PM-007 |

---

**Authority:** PM-007, Project Manager  
**Last Updated:** 2026-01-13  
**Next Review:** Before E02 execution resumes (2026-01-15 target)
