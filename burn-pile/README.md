# Burn Pile – Temporary Working Files

This folder holds temporary analysis documents, working drafts, and diagnostic outputs created during research, decision-making, or exploration—but that do not belong in the project root directory.

## What Goes Here

- **Analysis documents** – Comparative studies, option evaluations, JD assessments
- **Working drafts** – Early explorations that informed official deliverables
- **Diagnostic outputs** – Performance models, prototype findings, experimental results
- **Decision-making artifacts** – Reference matrices, tradeoff analyses, planning notes
- **Research explorations** – Options considered, dead ends, learning documents

## What Does NOT Go Here

- Official deliverables (those go in `roadmap/`)
- Governance templates (those go in `governance/`)
- Evidence artifacts (those go in `evidence/` or `roadmap/.../evidence/`)
- Test results or logs from task execution (those go in `evidence/`)

## Custodial Rules

1. **Add a header comment** to each file indicating its purpose and when it was created
2. **Link back to related official documents** if the work was incorporated into a deliverable
3. **Review quarterly** – Delete files that are no longer needed or whose decision has been made
4. **Do not commit to long-term storage** – This folder is explicitly temporary

## Examples

**File:** `JD_ANALYSIS_DEV033_DEV034.md`
```markdown
# Analysis: SQL Specialist JD Integration

**Purpose:** Evaluate fit of new specialized JDs (DEV-033, DEV-034) for E02 tasks
**Created:** 2026-01-14
**Status:** ✅ Complete – Analysis incorporated into E02 task reassignments
**Related Official Docs:** T02.3.2_JD-DEV034_..., T02.3.3_JD-DEV033_...
**Ready for deletion when:** E02 tasks are complete and reassignment has been validated in production
```

---

**Principle:** Keep the project root clean. Temporary work has a home here; it serves a purpose, then gets cleaned up.
