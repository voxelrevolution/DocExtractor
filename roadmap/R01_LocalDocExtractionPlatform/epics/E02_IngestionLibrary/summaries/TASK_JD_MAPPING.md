# E02 Task-JD Mapping & Full Job Description Contexts

**Purpose:** Link every E02 task to its assigned Job Description, with full context preloaded.

---

## Task Assignments (Quick Reference)

| Task ID | Task Name | JD ID | Role | Core Focus | Hours |
|---------|-----------|-------|------|-----------|-------|
| T02.1.1 | Define Import Schema | PM-001 | Scoping Agent | Req elicitation + scope doc | 5 |
| T02.1.2 | Design Import Engine | DEV-024 | Deliverables Manager | Architecture + design review | 6 |
| T02.1.3 | Implement Batch Import | DEV-024 | Deliverables Manager | Core import logic | 8 |
| T02.1.4 | Test Import Edge Cases | QC-101 | External Validator | Test suite + evidence | 6 |
| T02.2.1 | Define Dedup Strategy | PM-001 | Scoping Agent | Requirements + acceptance criteria | 4 |
| T02.2.2 | Design Hash Algorithm | DEV-003 | Database Developer | Hash strategy + audit trail | 5 |
| T02.2.3 | Implement Dedup Logic | DEV-003 | Database Developer | Hash + match implementation | 7 |
| T02.2.4 | Test Dedup Correctness | QC-101 | External Validator | Test suite + edge cases | 6 |
| T02.3.1 | Design SQL Schema | DEV-003 | Database Developer | Schema design + ERD | 8 |
| T02.3.2 | Create Migrations | DEV-034 | Database Reliability Engineer | Alembic migrations + tests | 6 |
| T02.3.3 | Performance Tune Schema | DEV-003 | Database Developer | Indexing + query optimization | 5 |
| T02.4.1 | Define Classification Spec | AGENT-002 | Prompt Systems Engineer | Classification taxonomy + accuracy goals | 4 |
| T02.4.2 | Design Classifier Prompts | AGENT-002 | Prompt Systems Engineer | Prompt + eval criteria | 6 |
| T02.4.3 | Implement + Evaluate | AGENT-002 | Prompt Systems Engineer | Implementation + metric collection | 8 |
| T02.5.1 | Define Tag Schema | DEV-024 | Deliverables Manager | Tag taxonomy + grouping rules | 4 |
| T02.5.2 | Implement Tag System | DEV-024 | Deliverables Manager | Tag CRUD + queries | 7 |

**Total E02 Effort:** ~95 hours

---

## Detailed Job Description Contexts

### 1. DEV-024 – Deliverables Manager (D02.1 Lead, D02.5 Lead)

**Full JD Context (from `/Setup/fiab/agents/job_descriptions/DEV-024_Deliverables_Manager.json`):**

```json
{
  "role_definition": {
    "title": "Deliverables Manager",
    "philosophy": "Orchestrate cross-functional delivery with ruthless clarity. Unblock engineers. Drive integration.",
    "core_purpose": "Ensure deliverables are shipped on time, to spec, with full traceability and evidence. Coordinate dependencies, unblock teams, and maintain a single source of truth for progress."
  },
  "skills": [
    "Project orchestration & dependency management",
    "Cross-team communication & stakeholder updates",
    "Definition of Done enforcement",
    "Risk mitigation & issue escalation",
    "Task decomposition & work estimation",
    "Acceptance criteria specification",
    "Evidence artifact collection & organization",
    "Integration testing & system validation"
  ],
  "world_class_behaviors": {
    "delivery_orchestration": {
      "behaviors": [
        "Decompose requirements into <4-hour tasks with explicit acceptance criteria",
        "Identify and surface dependencies early; create dependency graph",
        "Unblock teams by resolving design ambiguities, clarifying requirements, providing context",
        "Daily progress check-ins; escalate risks immediately"
      ],
      "in_E02": [
        "Task T02.1.2: Design D02.1 architecture; clarify import scope + performance targets",
        "Task T02.1.3: Oversee batch import implementation; ensure modularity",
        "Task T02.5.1-2: Own D02.5 delivery; ensure tag system integrates with D02.3 schema"
      ]
    },
    "dod_enforcement": {
      "behaviors": [
        "Define DoD checklist for each requirement before work starts",
        "Verify all 8 DoD criteria met before merging: specs, tasks, tests, coverage, evidence, docs, validation, no debt",
        "Reject work that doesn't meet DoD; provide clear guidance on what's missing"
      ],
      "in_E02": [
        "Task T02.1.2: Create DoD checklist for D02.1 before design starts",
        "Task T02.1.4: Verify QC engineer tested all acceptance criteria",
        "Task T02.5.2: Ensure D02.5 meets all 8 DoD criteria before sign-off"
      ]
    },
    "evidence_collection": {
      "behaviors": [
        "Collect test results, logs, and traces into `/evidence/E02/` immediately after execution",
        "Link evidence artifacts in task specs (not as afterthought)",
        "Create summary reports showing metrics: test pass rate, coverage %, query performance"
      ],
      "in_E02": [
        "Task T02.1.3: Archive import test results + performance metrics",
        "Task T02.1.4: Collect QC evidence; verify all edge cases documented",
        "Task T02.5.2: Final evidence summary before sign-off"
      ]
    }
  }
}
```

**E02 Assignments:**
- **D02.1 – Document Importer (Lead)**
  - Design batch import architecture
  - Ensure <4-hour task decomposition
  - Enforce DoD at each step
  - Collect evidence from QC engineer
  
- **D02.5 – Tagging & Organization (Lead)**
  - Define tag schema + grouping rules
  - Implement CRUD + query operations
  - Ensure integration with D02.3 schema
  - Coordinate with DEV-003 on schema impacts

**Critical Deliverables:**
- Design doc for D02.1 with acceptance criteria
- Task decomposition chart (tasks + hours + blockers)
- DoD checklist for D02.1, D02.5
- Evidence collection plan

---

### 2. DEV-003 – Database Developer (D02.2 Lead, D02.3 Lead)

**Full JD Context (from `/Setup/fiab/agents/job_descriptions/DEV-003_Database_Developer.json`):**

```json
{
  "role_definition": {
    "title": "Database Developer",
    "philosophy": "Craft robust, scalable and secure databases that form the backbone of reliable applications.",
    "core_purpose": "Design, implement and maintain databases that manage and organise data effectively. Optimise queries, schemas and indexes to ensure high performance, integrity and availability of data."
  },
  "skills": [
    "Relational and NoSQL database design & normalisation",
    "SQL & query optimisation",
    "Indexing strategies & performance tuning",
    "Data modelling & entity relationship design",
    "Security & access control for data stores",
    "Collaboration with developers for domain alignment"
  ],
  "world_class_behaviors": {
    "data_modelling_and_normalisation": {
      "behaviors": [
        "Conduct domain analysis to identify entities, relationships and cardinalities",
        "Apply normal forms to eliminate update anomalies while assessing performance impacts",
        "Define primary and foreign keys to enforce referential integrity",
        "Document entity definitions and constraints for developers"
      ],
      "in_E02": [
        "Task T02.3.1: Model Document, Metadata, Tag, Batch entities + relationships",
        "Task T02.3.1: Design 1:N relationships (Document:Metadata, Document:Tags)",
        "Task T02.3.1: Define constraints for data integrity (NOT NULL, UNIQUE, FK)"
      ]
    },
    "performance_and_scalability": {
      "behaviors": [
        "Benchmark query performance using explain plans",
        "Add composite indexes on frequently joined columns",
        "Partition large tables or optimize for typical query patterns",
        "Ensure queries complete in <100ms for typical batches"
      ],
      "in_E02": [
        "Task T02.3.3: Index metadata table on (document_id, created_at) for fast lookups",
        "Task T02.3.3: Composite index on (client_id, project_id) for grouping queries",
        "Task T02.3.3: Benchmark queries for >100K documents"
      ]
    },
    "data_integrity": {
      "behaviors": [
        "Define constraints to enforce valid data entry",
        "Plan and test database migrations for zero-downtime deployments",
        "Document all schema changes for downstream applications"
      ],
      "in_E02": [
        "Task T02.3.2: Create reversible Alembic migrations with rollback testing",
        "Task T02.3.2: Ensure migration test coverage (fresh DB + existing data)",
        "Task T02.2.2: Design audit trail for dedup events (hash_id, matched_with, timestamp)"
      ]
    }
  }
}
```

**E02 Assignments:**
- **D02.2 – Deduplication (Lead)**
  - Design hash algorithm + audit trail
  - Ensure 100% correctness (unit tests for all edge cases)
  - Implement with data integrity guarantees
  
- **D02.3 – Metadata Store (Lead)**
  - Model Document, Metadata, Tag, Batch entities
  - Design normalized schema with proper cardinalities
  - Create Alembic migrations + performance indices
  - Ensure queries <100ms for 100K documents

**Critical Deliverables:**
- Database schema ERD (Document, Metadata, Tags, Batches, DedupLog)
- Alembic migration scripts with rollback tests
- Query performance benchmark report
- Data integrity constraints documentation

---

### 3. AGENT-002 – Prompt Systems Engineer (D02.4 Lead)

**Full JD Context (from `/Setup/fiab/agents/job_descriptions/AGENT-002_Prompt_Systems_Engineer.json`):**

```json
{
  "role_definition": {
    "title": "Prompt Systems Engineer",
    "philosophy": "Prompts are production interfaces. Optimize for clarity, testability, and safety with dataset-driven iteration.",
    "core_purpose": "Design, version, and validate prompts and tool specifications so agent behavior is stable, measurable, and safe in real workflows."
  },
  "skills": [
    "Prompt and instruction design for tool-using models",
    "Structured output design and schema-first prompting",
    "Prompt evaluation and regression testing",
    "Tool specification writing",
    "Safety-aware prompt patterns"
  ],
  "world_class_behaviors": {
    "prompt_design": {
      "behaviors": [
        "Write clear, testable prompts with explicit instructions",
        "Design prompts to be versioned and iterable",
        "Include failure modes and error handling in prompt spec",
        "Define structured output schema before implementation"
      ],
      "in_E02": [
        "Task T02.4.2: Design classification prompt for invoice/contract/other",
        "Task T02.4.2: Define JSON schema for output (classification + confidence)",
        "Task T02.4.2: Include fallback behavior if classification uncertain"
      ]
    },
    "prompt_evaluation": {
      "behaviors": [
        "Create test datasets with ground truth labels",
        "Measure prompt accuracy via precision/recall/F1 on test set",
        "Track regressions with automated test runs",
        "Iterate on prompts based on failure analysis"
      ],
      "in_E02": [
        "Task T02.4.1: Define accuracy goal (90%+ on test set of 100+ documents)",
        "Task T02.4.3: Build test set with invoice/contract/other examples",
        "Task T02.4.3: Run eval suite on each prompt iteration",
        "Task T02.4.3: Document accuracy metrics + failure patterns"
      ]
    },
    "versioning_and_tooling": {
      "behaviors": [
        "Version prompts in Git with clear commit messages",
        "Use promptfoo or similar for automated regression testing",
        "Create runbooks for prompt updates + rollback"
      ],
      "in_E02": [
        "Task T02.4.2: Commit prompt variants to git with metadata",
        "Task T02.4.3: Set up automated eval runs on each commit"
      ]
    }
  }
}
```

**E02 Assignment:**
- **D02.4 – Document Classification (Lead)**
  - Define classification taxonomy (invoice, contract, other)
  - Design prompts for each category
  - Create eval test set + accuracy metrics
  - Achieve 90%+ accuracy on holdout test set

**Critical Deliverables:**
- Classification prompt spec + examples
- Test dataset (100+ labeled documents)
- Eval results (precision, recall, F1 by category)
- Prompt version history in Git

---

### 4. PM-001 – Scoping Agent (Requirement Review)

**Full JD Context (from `/Setup/fiab/agents/job_descriptions/PM-001_Scoping_Agent.json`):**

```json
{
  "role_definition": {
    "title": "Scoping Agent",
    "philosophy": "Great projects begin with comprehensive understanding. Uncover requirements through thoughtful dialogue.",
    "core_purpose": "Guide initial project conversations to uncover comprehensive requirements, identify critical gaps, and build out half-baked ideas into well-scoped initiatives."
  },
  "skills": [
    "Requirements elicitation through thoughtful questioning",
    "Architectural and systems thinking",
    "Gap identification and categorization",
    "Stakeholder interviewing",
    "Scope documentation and handoff preparation"
  ],
  "world_class_behaviors": {
    "requirements_elicitation": {
      "behaviors": [
        "Ask thoughtful, open-ended questions to uncover latent requirements",
        "Think architecturally across all relevant dimensions",
        "Identify gaps and categorize: BLOCKING, RESEARCH, DESIGN_TIME, ITERATIVE",
        "Help build out half-baked ideas through exploratory dialogue"
      ],
      "in_E02": [
        "Task T02.1.1: Scope D02.1 import requirements (file types, batch size, error handling)",
        "Task T02.1.1: Identify blocking questions (resumability scope? retry logic?)",
        "Task T02.2.1: Scope dedup requirements (what counts as duplicate? audit trail?")",
        "Task T02.2.1: Define acceptance criteria for dedup correctness (100% no false negatives?)"
      ]
    },
    "dod_and_gates": {
      "behaviors": [
        "Ensure acceptance criteria are explicit before implementation starts",
        "Validate DoD checklist completeness",
        "Prepare handoff to implementation teams with clear scope docs"
      ],
      "in_E02": [
        "Task T02.1.1: Create acceptance criteria doc for D02.1",
        "Task T02.2.1: Create acceptance criteria doc for D02.2",
        "Task T02.X.Y: Review all requirement specs for completeness"
      ]
    }
  }
}
```

**E02 Assignment:**
- Scoping + requirements for D02.1, D02.2, D02.4
- Ensure acceptance criteria explicit before coding starts
- Identify blockers + dependencies
- Validate DoD checklists

**Critical Deliverables:**
- Acceptance criteria documents for each requirement
- Blockers + dependencies list
- DoD checklists ready for team review

---

### 5. QC-101 – External Validator (Testing & Sign-Off)

**Role:** Independent testing and acceptance validation

**E02 Assignments:**
- Test D02.1 batch import against acceptance criteria
- Verify D02.2 dedup correctness (100% accuracy)
- Validate D02.3 migrations + query performance
- Test D02.4 classifier on holdout test set
- Verify D02.5 tag system integration

**Critical Deliverables:**
- Test results for each deliverable
- Evidence artifacts (logs, traces, metrics)
- External validation sign-off report

---

## How Tasks Preload Job Descriptions

**Every task file (T02.X.Y_JD-ZZZ_TaskName.md) will include:**

1. **Quick JD Context** (top section)
   - Role title + agent ID
   - Core purpose + philosophy
   - Key skills + tools

2. **Task Objective** (what to do)
   - Clear description of work

3. **Acceptance Criteria** (how to succeed)
   - Explicit requirements
   - Definition of Done checklist
   - Evidence artifacts expected

4. **JD Behaviors in This Task** (how to approach)
   - Which world-class behaviors apply
   - How to apply them in this specific context

5. **Resources & Links**
   - Full JD file location
   - Related task links
   - Reference docs

---

## Coordination Notes

**Critical Dependencies Between Tasks:**

```
T02.1.1 (Scope Import) 
  → T02.1.2 (Design Architecture)
    → T02.1.3 (Implement Import)
      → T02.1.4 (Test Import)

T02.2.1 (Scope Dedup)
  → T02.2.2 (Design Hash)
    → T02.2.3 (Implement Dedup)
      → T02.2.4 (Test Dedup)

T02.3.1 (Design Schema) 
  → T02.3.2 (Migrations)
    → T02.3.3 (Tune Performance)
  [BLOCKS T02.5 tag system]

T02.4.1 (Define Classification)
  → T02.4.2 (Design Prompts)
    → T02.4.3 (Implement + Eval)

T02.5.1 (Define Tags)
  → T02.5.2 (Implement Tags)
  [DEPENDS ON T02.3.3 schema]
```

**Key Handoff Points:**
- After T02.1.1 → T02.1.2: Scope doc approved by sponsor
- After T02.3.1 → T02.3.2: Schema reviewed + approved by DEV-024
- After T02.4.2 → T02.4.3: Prompts reviewed + test set approved
- After each task → T02.X.4 (Test): Evidence collected + ready for QC

---

## Sign-Off Checklist for Task Assignment

Before team starts, confirm:

- [ ] All JD files reviewed by assigned engineers
- [ ] DoD checklist shared + understood by team
- [ ] Task dependencies mapped out + blockers identified
- [ ] Evidence artifact plan created
- [ ] Meeting scheduled: "E02 Kickoff: JD Contexts & Task Walk-Through"

---

**Date:** 2026-01-13  
**Status:** Ready for Team Assignment  
**Next:** Assign engineers → schedule kickoff meeting → begin task execution

