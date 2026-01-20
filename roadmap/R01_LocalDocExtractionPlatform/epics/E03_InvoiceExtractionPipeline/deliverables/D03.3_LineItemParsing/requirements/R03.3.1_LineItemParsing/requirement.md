# R03.3.1_LineItemParsing

**Status:** QC Pending  
**JD Owners:** DATA-026  
**Due:** [TBD]

## Definition

Implement table-aware line item parsing with provenance for invoice line items.

**Acceptance Criteria:**
- Line items extracted with stable row ordering.
- Evidence pointers present for each line item.
- Failure modes documented and review routing defined.

---

## Tasks

- T03.3.1_JD-DATA026_LineItemParsing.md

## Evidence

- Heuristic line item parsing implemented (src/extraction/invoice.py)
- Design: T03.3.1_JD-DATA026_Design.md
- Implementation: T03.3.1_JD-DATA026_Implementation.md
- Test Results: T03.3.1_JD-DATA026_TestResults.md
- Completion Summary: T03.3.1_JD-DATA026_CompletionSummary.md

---

## Reference

- **Evidence Location:** ../evidence/R03.3.1_LineItemParsing/
