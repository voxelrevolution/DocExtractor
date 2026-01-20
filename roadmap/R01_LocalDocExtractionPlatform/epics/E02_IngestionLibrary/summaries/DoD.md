# E02 Definition of Done (DoD) – Front-Loaded Quality Gate

**Purpose:** Every deliverable must satisfy ALL criteria before sign-off. This is not an afterthought.

---

## DoD Structure

Each requirement in E02 must pass **8 mandatory quality gates** before merging:

1. **Requirement Specs Complete** – Acceptance criteria explicit, no ambiguity
2. **Tasks Decomposed** – All work broken into <4-hour tasks with JD assignments
3. **Tests Written** – Before or alongside code; minimum 80% coverage
4. **Job Descriptions Preloaded** – Every task includes full JD context
5. **Evidence Artifacts Collected** – Test results, logs, metrics in `/evidence/E02/`
6. **Documentation Updated** – README, schemas, API docs current
7. **External Validation Passed** – QC engineer confirms against acceptance criteria
8. **No Technical Debt** – Code follows modularity; no shortcuts or workarounds

**If any gate fails, requirement is NOT done. No exceptions.**

---

## Requirement-by-Requirement DoD Checklist

### R02.1: Batch Import (D02.1)

**Acceptance Criteria:**
- [ ] Single file import works (PDF, XLSX, DOCX, PNG/JPG)
- [ ] Batch import works for 10, 100, 1000 files
- [ ] Progress is trackable (X of Y files processed)
- [ ] Process can resume after interruption
- [ ] Errors are logged + user-visible (no silent failures)
- [ ] Import time <500ms per file (avg)

**Tasks Assigned:**
- T02.1.1: Define import spec (PM-001, 5 hrs)
- T02.1.2: Design architecture (DEV-024, 6 hrs)
- T02.1.3: Implement logic (DEV-024, 8 hrs)
- T02.1.4: Test edge cases (QC-101, 6 hrs)

**DoD Checklist for R02.1:**
- [ ] **Specs:** Acceptance criteria above + architecture doc approved by DEV-024
- [ ] **Tasks:** All 4 tasks estimated + dependencies mapped
- [ ] **Tests:** 
  - [ ] Unit tests: single file import (all file types)
  - [ ] Unit tests: batch import (10, 100, 1K files)
  - [ ] Unit tests: progress tracking + resumability
  - [ ] Unit tests: error handling + logging
  - [ ] Integration tests: end-to-end import workflow
  - [ ] Performance tests: <500ms/file on typical system
  - [ ] Test coverage: 80%+ code coverage measured
- [ ] **JD Preloading:**
  - [ ] T02.1.2: DEV-024 context preloaded (orchestration, DoD, evidence)
  - [ ] T02.1.3: DEV-024 context preloaded (delivery, unblocking)
  - [ ] T02.1.4: QC-101 context preloaded (acceptance testing)
- [ ] **Evidence:**
  - [ ] Test results (`/evidence/E02/R02.1_test_results.txt`)
  - [ ] Coverage report (`/evidence/E02/R02.1_coverage.html`)
  - [ ] Performance metrics (`/evidence/E02/R02.1_perf_benchmark.csv`)
  - [ ] Resumability test log (`/evidence/E02/R02.1_resumability.log`)
- [ ] **Documentation:**
  - [ ] README updated with import example
  - [ ] API docs updated (import endpoints)
  - [ ] Schema diagram updated (if new DB tables)
- [ ] **External Validation:**
  - [ ] QC-101 ran all tests; 100% pass
  - [ ] QC-101 verified resumability works
  - [ ] QC-101 signed acceptance form
- [ ] **No Debt:**
  - [ ] No hardcoded paths or config
  - [ ] Logging follows project standards
  - [ ] Error messages are user-friendly
  - [ ] Code is modular (can extend to new file types)

**Sign-Off:** DEV-024 (impl) + QC-101 (validation) + PM-001 (spec)

---

### R02.2: Deduplication (D02.2)

**Acceptance Criteria:**
- [ ] Duplicate detection is 100% accurate (no false negatives allowed)
- [ ] Hashing algorithm deterministic (same file = same hash)
- [ ] Audit trail records all dedup events (who, when, which docs matched)
- [ ] Conflict resolution: users can mark as NOT a duplicate if false positive
- [ ] Performance: <1 second for 10K documents

**Tasks Assigned:**
- T02.2.1: Define dedup spec (PM-001, 4 hrs)
- T02.2.2: Design hash algorithm (DEV-003, 5 hrs)
- T02.2.3: Implement dedup (DEV-003, 7 hrs)
- T02.2.4: Test correctness (QC-101, 6 hrs)

**DoD Checklist for R02.2:**
- [ ] **Specs:** Dedup algorithm documented (hash function, collision handling, audit trail design)
- [ ] **Tasks:** All 4 tasks estimated + dependencies clear
- [ ] **Tests:**
  - [ ] Unit tests: hash function determinism (same file → same hash)
  - [ ] Unit tests: collision detection (near-duplicates + exact matches)
  - [ ] Unit tests: false negative coverage (all edge cases)
  - [ ] Unit tests: audit trail correctness
  - [ ] Unit tests: conflict resolution workflow
  - [ ] Integration tests: dedup on real document batches
  - [ ] Performance tests: <1 sec for 10K docs
  - [ ] Test coverage: 85%+ code coverage
- [ ] **JD Preloading:**
  - [ ] T02.2.2: DEV-003 context (DB design, data integrity)
  - [ ] T02.2.3: DEV-003 context (implementation, testing)
- [ ] **Evidence:**
  - [ ] Test results (`/evidence/E02/R02.2_test_results.txt`)
  - [ ] Coverage report (`/evidence/E02/R02.2_coverage.html`)
  - [ ] Performance metrics (`/evidence/E02/R02.2_perf_10k.csv`)
  - [ ] Audit trail sample (`/evidence/E02/R02.2_audit_trail_sample.json`)
  - [ ] Edge case analysis (`/evidence/E02/R02.2_edge_cases.md`)
- [ ] **Documentation:**
  - [ ] Dedup algorithm doc (hash function, collision rules)
  - [ ] Audit trail schema documented
  - [ ] API docs updated (dedup endpoints)
- [ ] **External Validation:**
  - [ ] QC-101 verified 100% accuracy on test set
  - [ ] QC-101 tested false negative edge cases
  - [ ] QC-101 verified audit trail completeness
  - [ ] QC-101 signed acceptance
- [ ] **No Debt:**
  - [ ] Hash algorithm is reversible/standard (no custom crypto)
  - [ ] Audit trail is immutable (append-only)
  - [ ] Conflict resolution is user-friendly

**Sign-Off:** DEV-003 (impl) + QC-101 (validation) + PM-001 (spec)

---

### R02.3: Metadata Store (D02.3)

**Acceptance Criteria:**
- [ ] PostgreSQL schema captures Document, Metadata, Tags, Batches
- [ ] Schema is normalized (no data duplication)
- [ ] Migrations are reversible + tested
- [ ] Queries complete in <100ms for 100K documents
- [ ] Indices are optimized for typical query patterns

**Tasks Assigned:**
- T02.3.1: Design schema (DEV-003, 8 hrs)
- T02.3.2: Create migrations (DEV-034, 6 hrs)
- T02.3.3: Tune performance (DEV-003, 5 hrs)

**DoD Checklist for R02.3:**
- [ ] **Specs:** 
  - [ ] Schema ERD complete (entities, relationships, cardinalities)
  - [ ] Data dictionary documented (all columns)
  - [ ] Constraints documented (PKs, FKs, NOT NULLs, UNIQUEs)
- [ ] **Tasks:** All 3 tasks estimated + design review completed
- [ ] **Tests:**
  - [ ] Schema tests: create, read, update, delete all entities
  - [ ] Schema tests: foreign key constraints enforced
  - [ ] Schema tests: indices exist + are used by query planner
  - [ ] Migration tests: forward migration works on fresh DB
  - [ ] Migration tests: backward migration (rollback) works
  - [ ] Migration tests: migration idempotent (run twice = same result)
  - [ ] Performance tests: queries <100ms for 100K docs
  - [ ] Test coverage: 90%+ coverage on migration logic
- [ ] **JD Preloading:**
  - [ ] T02.3.1: DEV-003 context (data modeling, normalization, performance)
  - [ ] T02.3.2: DEV-034 context (data integrity, migrations, reliability)
  - [ ] T02.3.3: DEV-003 context (performance tuning, indexing)
- [ ] **Evidence:**
  - [ ] Schema ERD diagram (`/evidence/E02/R02.3_schema_erd.png`)
  - [ ] Data dictionary (`/evidence/E02/R02.3_data_dictionary.md`)
  - [ ] Migration test results (`/evidence/E02/R02.3_migration_tests.txt`)
  - [ ] Performance benchmark (`/evidence/E02/R02.3_query_perf_100k.csv`)
  - [ ] Index analysis (`/evidence/E02/R02.3_index_usage.sql`)
- [ ] **Documentation:**
  - [ ] Schema diagram in `/docs/ARCHITECTURE.md`
  - [ ] Data dictionary in project docs
  - [ ] Migration naming convention documented
  - [ ] Query performance guide for developers
- [ ] **External Validation:**
  - [ ] QC-101 verified schema normalization
  - [ ] QC-101 tested all migrations (forward + rollback)
  - [ ] QC-101 validated query performance on 100K+ rows
  - [ ] QC-101 signed acceptance
- [ ] **No Debt:**
  - [ ] No hardcoded SQL or table names in code
  - [ ] All migrations use Alembic (not manual SQL)
  - [ ] Indices are documented (reason for each)

**Sign-Off:** DEV-003 (impl) + QC-101 (validation)

---

### R02.4: Classification v1 (D02.4)

**Acceptance Criteria:**
- [ ] Classifier identifies invoice, contract, or other with 90%+ accuracy
- [ ] Prompts are versioned in Git
- [ ] Test set includes 100+ labeled examples
- [ ] Eval metrics tracked (precision, recall, F1 by category)
- [ ] Fallback behavior defined (uncertain → "other")

**Tasks Assigned:**
- T02.4.1: Define classification spec (AGENT-002, 4 hrs)
- T02.4.2: Design prompts (AGENT-002, 6 hrs)
- T02.4.3: Implement + evaluate (AGENT-002, 8 hrs)

**DoD Checklist for R02.4:**
- [ ] **Specs:**
  - [ ] Classification taxonomy defined (invoice, contract, other)
  - [ ] Accuracy goal: 90%+ F1 on test set
  - [ ] Structured output schema defined (JSON with classification + confidence)
- [ ] **Tasks:** All 3 tasks estimated + dependencies clear
- [ ] **Tests:**
  - [ ] Unit tests: prompt formatting + JSON parsing
  - [ ] Eval tests: accuracy on test set (100+ labeled docs)
  - [ ] Eval tests: per-category accuracy (precision, recall, F1)
  - [ ] Eval tests: fallback behavior (uncertain → "other")
  - [ ] Regression tests: accuracy on previous test set after any change
  - [ ] Test coverage: 80%+ code coverage (where applicable)
- [ ] **JD Preloading:**
  - [ ] T02.4.2: AGENT-002 context (prompt design, evaluation, versioning)
  - [ ] T02.4.3: AGENT-002 context (implementation, metrics, iteration)
- [ ] **Evidence:**
  - [ ] Test set (`/evidence/E02/R02.4_test_set.json` - 100+ labeled docs)
  - [ ] Prompt versions (Git history)
  - [ ] Eval results (`/evidence/E02/R02.4_eval_results.txt` - accuracy metrics)
  - [ ] Confusion matrix (`/evidence/E02/R02.4_confusion_matrix.csv`)
  - [ ] Failure analysis (`/evidence/E02/R02.4_failure_cases.md`)
- [ ] **Documentation:**
  - [ ] Prompt spec documented (intent, examples, fallback)
  - [ ] Classification taxonomy documented
  - [ ] Eval methodology documented
  - [ ] Results summary in project README
- [ ] **External Validation:**
  - [ ] QC-101 verified test set quality (good label coverage)
  - [ ] QC-101 ran eval suite independently; achieved 90%+ F1
  - [ ] QC-101 reviewed failure cases + approved tolerance
  - [ ] QC-101 signed acceptance
- [ ] **No Debt:**
  - [ ] Prompts are versioned (no magic strings)
  - [ ] Test set is reproducible
  - [ ] Eval scripts are repeatable
  - [ ] Failure cases documented for future iteration

**Sign-Off:** AGENT-002 (impl) + QC-101 (validation)

---

### R02.5: Tagging & Organization (D02.5)

**Acceptance Criteria:**
- [ ] Users can create tags and assign to documents
- [ ] Documents can be grouped by tag, client, project, batch
- [ ] Tag queries complete in <100ms for 10K documents
- [ ] Tag system integrates with D02.3 schema (FK relationships)
- [ ] UI allows bulk tagging + group operations

**Tasks Assigned:**
- T02.5.1: Define tag schema (DEV-024, 4 hrs)
- T02.5.2: Implement tag system (DEV-024, 7 hrs)

**DoD Checklist for R02.5:**
- [ ] **Specs:**
  - [ ] Tag schema defined (tag structure, cardinalities, constraints)
  - [ ] Grouping rules documented (by client, project, batch, tag)
  - [ ] Query patterns documented (list tags, get docs by tag, bulk assign)
- [ ] **Tasks:** All 2 tasks estimated + schema coordination with DEV-003 completed
- [ ] **Tests:**
  - [ ] Unit tests: create tag, assign to document
  - [ ] Unit tests: remove tag, bulk assign tags
  - [ ] Unit tests: query documents by tag, client, project, batch
  - [ ] Unit tests: tag constraints enforced (no duplicates, valid FK)
  - [ ] Performance tests: queries <100ms for 10K docs
  - [ ] Integration tests: tagging integrates with D02.1 (import + tag workflow)
  - [ ] Test coverage: 80%+ code coverage
- [ ] **JD Preloading:**
  - [ ] T02.5.1: DEV-024 context (design, coordination, DoD)
  - [ ] T02.5.2: DEV-024 context (implementation, integration, evidence)
- [ ] **Evidence:**
  - [ ] Test results (`/evidence/E02/R02.5_test_results.txt`)
  - [ ] Coverage report (`/evidence/E02/R02.5_coverage.html`)
  - [ ] Performance metrics (`/evidence/E02/R02.5_query_perf.csv`)
  - [ ] Integration test log (`/evidence/E02/R02.5_integration_test.log`)
- [ ] **Documentation:**
  - [ ] Tag schema diagram (included in D02.3 schema)
  - [ ] API docs: tag CRUD endpoints
  - [ ] Query examples in README
- [ ] **External Validation:**
  - [ ] QC-101 verified bulk tag operations
  - [ ] QC-101 tested grouping queries
  - [ ] QC-101 validated schema integration
  - [ ] QC-101 signed acceptance
- [ ] **No Debt:**
  - [ ] Tag operations are atomic (no partial updates)
  - [ ] Cascade deletes handled (delete tag → remove from docs)
  - [ ] UI-ready API (bulk operations supported)

**Sign-Off:** DEV-024 (impl) + QC-101 (validation)

---

## Master DoD Verification (Post-Execution)

**Before E02 sign-off, verify all requirements pass all gates:**

| Requirement | Specs | Tasks | Tests | JD Preload | Evidence | Docs | Validation | No Debt |
|---|---|---|---|---|---|---|---|---|
| R02.1 Batch Import | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| R02.2 Dedup | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| R02.3 Metadata Store | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| R02.4 Classification | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| R02.5 Tagging | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**All 8 gates must show ✅ for each requirement. No exceptions.**

---

## How to Use This Checklist

1. **At Task Start:** Copy the relevant DoD checklist into your task spec
2. **During Development:** Check off items as you complete them
3. **Before Pull Request:** Verify all items checked off
4. **During Code Review:** Reviewer verifies all DoD items satisfied
5. **After Merge:** Link evidence artifacts in the task spec

**If any item is unchecked, task is not ready for merge.**

---

**Date:** 2026-01-13  
**Status:** Ready for Team Use  
**Enforcement:** DEV-024 + QC-101

