# E01 Kickoff Package – Core Foundation

## Epic Context
E01 establishes the development environment, local LLM runtime integration, observability, and core data schemas that all downstream epics depend on. This is a **blocking dependency**—no other work can begin until E01 exits (tests passing, all DoD met).

## Tech Stack (Locked)
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Backend | FastAPI (Python 3.11+) + Pydantic | Type-safe, async APIs, excellent for local services |
| Frontend | Tauri + React/TypeScript | Native desktop app, local web UI, zero cloud |
| Database | PostgreSQL (local) + pgvector | Robust ACID, vector search for semantic queries |
| LLM Runtime | Ollama + Mixtral 8x7b | Structured extraction, proven JSON output |
| Vector Embeddings | pgvector + sentence-transformers | Semantic search, corpus similarity |
| Observability | OpenTelemetry + local collector | Full traceability, no cloud export |
| CI/CD | GitHub Actions (local runners) | Tests on every commit |

## Deliverables (E01)

### D01.1 – Development Environment Setup
- [ ] Python 3.11+ venv creation and dependency locking (requirements.txt)
- [ ] PostgreSQL local instance (Docker or native)
- [ ] Ollama model initialization (Mixtral 8x7b pulled and verified)
- [ ] IDE/editor config (VSCode settings, Python linting, formatting)
- [ ] Onboarding runbook (how to get a fresh dev machine ready in <30 min)

### D01.2 – Local Model Runtime (Ollama Integration)
- [ ] Python client library integration (ollama-py or similar)
- [ ] Model loading and health check
- [ ] Structured output enforcement (JSON schema validation)
- [ ] Token counting and context window management
- [ ] Inference latency profiling and logging

### D01.3 – Observability & Telemetry
- [ ] OpenTelemetry SDK integration (Python)
- [ ] Trace exporter (local OTLP collector or console-based)
- [ ] Structured logging (JSON logs with correlation IDs)
- [ ] Metrics collection (request latency, inference time, errors)
- [ ] Dashboard/UI for trace inspection (Jaeger or similar, local)

### D01.4 – Evidence & Citation Schema Design
- [ ] JSON schema for evidence pointers (document ID, page, region, confidence)
- [ ] Extraction result schema (field name, value, evidence list, timestamp)
- [ ] Annotation schema (user corrections, feedback, feedback type)
- [ ] Validation tests for all schemas
- [ ] Documentation (how to cite evidence in extraction pipelines)

### D01.5 – Core Data Types & Interfaces
- [ ] Document interface (id, path, content, metadata, ingestion timestamp)
- [ ] ExtractionResult interface (document_id, fields, evidence, version)
- [ ] Annotation interface (extraction_id, field_name, correction, reason)
- [ ] Query interfaces for database (document lookup, evidence search, annotation retrieval)
- [ ] Type stubs and validation layer

### D01.6 – CI/CD & Test Infrastructure
- [ ] pytest setup with fixtures (mock Ollama, test DB)
- [ ] GitHub Actions workflow (test on every push)
- [ ] Coverage reporting and minimum thresholds (80%+)
- [ ] Artifact storage for test evidence (logs, trace files)
- [ ] Local test runner documentation

## Requirements (E01)

### R01.1 – Dev Environment Reproducibility
**Acceptance Criteria:**
- [ ] A fresh clone + `./scripts/setup.sh` completes in <30 minutes on a clean machine
- [ ] All dependencies pinned to exact versions (requirements.txt, psql version, Ollama version)
- [ ] Onboarding doc exists and is tested by at least one external party
- [ ] Setup script detects missing dependencies and gives clear error messages

**Definition of Done:** See [DoD.md](#r0101-dod)

### R01.2 – Ollama Integration & Model Loading
**Acceptance Criteria:**
- [ ] Python client successfully connects to local Ollama on startup
- [ ] Mixtral 8x7b model loads and responds to test prompts within 5 seconds
- [ ] Structured output (JSON) enforced; malformed responses rejected
- [ ] Token counting is accurate (used for prompt/context planning)
- [ ] Inference latency is logged per request

**Definition of Done:** See [DoD.md](#r0102-dod)

### R01.3 – Observability for All Traces
**Acceptance Criteria:**
- [ ] Every API call is traced with correlation ID
- [ ] LLM inference calls include prompt, response, latency, token counts
- [ ] Database queries logged with execution time
- [ ] All traces exportable to JSON for debugging
- [ ] Trace viewer accessible locally (Jaeger or equivalent)

**Definition of Done:** See [DoD.md](#r0103-dod)

### R01.4 – Evidence Schema Validated
**Acceptance Criteria:**
- [ ] Evidence pointers survive round-trip serialization (JSON→Python→JSON)
- [ ] Confidence scores always in range [0, 1]
- [ ] Page numbers and regions validated against actual document bounds
- [ ] Schema enforced at entry point (FastAPI request validation)
- [ ] Example extraction results with evidence pass schema tests

**Definition of Done:** See [DoD.md](#r0104-dod)

### R01.5 – Core Data Types Testable
**Acceptance Criteria:**
- [ ] All data types have working `__eq__` and serialization
- [ ] Database ORM models (SQLAlchemy) map cleanly to Pydantic schemas
- [ ] Queries return typed results (not raw dicts)
- [ ] Type hints cover 100% of public APIs
- [ ] mypy runs with strict mode, zero errors

**Definition of Done:** See [DoD.md](#r0105-dod)

### R01.6 – Tests Run on Every Commit
**Acceptance Criteria:**
- [ ] GitHub Actions workflow executes all tests on every push
- [ ] Tests pass or workflow fails (no partial success)
- [ ] Coverage report generated and stored
- [ ] Failing tests block merge (if using PR protection)
- [ ] Test artifact logs available for inspection

**Definition of Done:** See [DoD.md](#r0106-dod)

## Definition of Done (DoD) by Requirement

### R01.1 DoD
- [ ] `./scripts/setup.sh` is executable and idempotent
- [ ] Runs to completion with zero manual intervention
- [ ] Validates all dependencies (Python, PostgreSQL, Ollama)
- [ ] Creates venv, installs packages, initializes database
- [ ] Onboarding doc exists in `docs/ONBOARDING.md`
- [ ] At least one non-author has successfully run setup
- [ ] All changes documented in `CHANGELOG.md`
- [ ] Tests: `test_setup.py` verifies venv creation and dependency versions
- [ ] Evidence: Setup logs from test run stored in `evidence/setup_logs/`

### R01.2 DoD
- [ ] Python module `src/llm/client.py` created with `OllamaClient` class
- [ ] `OllamaClient.load_model()` successfully loads Mixtral 8x7b
- [ ] `OllamaClient.infer(prompt: str, schema: dict) -> dict` validates output against schema
- [ ] Token counting implemented and tested
- [ ] All inference calls logged with latency and token counts
- [ ] Tests: `test_ollama_client.py` covers happy path, model load failure, schema violations
- [ ] Evidence: Test output showing successful model load, latency metrics

### R01.3 DoD
- [ ] OpenTelemetry SDK initialized in `src/observability/telemetry.py`
- [ ] Trace exporter configured (OTLP collector or console)
- [ ] Correlation IDs generated and propagated across all API calls
- [ ] FastAPI middleware adds traces to all endpoints
- [ ] All database queries traced
- [ ] All LLM inference calls traced with full context
- [ ] Tests: `test_observability.py` verifies trace generation and export
- [ ] Evidence: Sample trace JSON files showing complete workflow

### R01.4 DoD
- [ ] JSON schema file: `src/schemas/evidence.json` (Evidence pointer format)
- [ ] JSON schema file: `src/schemas/extraction_result.json`
- [ ] JSON schema file: `src/schemas/annotation.json`
- [ ] Pydantic models created for all three schemas
- [ ] Round-trip validation tests passing
- [ ] FastAPI endpoints reject invalid evidence via 422 response
- [ ] Example extraction results with evidence provided and validated
- [ ] Tests: `test_evidence_schema.py` covers all schema validations
- [ ] Evidence: Sample valid and invalid evidence pointers with test output

### R01.5 DoD
- [ ] SQLAlchemy ORM models created for: Document, ExtractionResult, Annotation
- [ ] Corresponding Pydantic schemas created for API serialization
- [ ] All public methods have type hints (mypy strict mode passing)
- [ ] `__eq__` and serialization tested for all types
- [ ] Database queries return typed dataclass/Pydantic models
- [ ] Tests: `test_data_types.py` covers instantiation, equality, serialization
- [ ] Evidence: mypy output showing zero errors

### R01.6 DoD
- [ ] `.github/workflows/test.yml` created with pytest, coverage, artifact upload
- [ ] Tests run on every push to `main` and all PRs
- [ ] Coverage report published (e.g., to artifacts)
- [ ] Workflow failure blocks PR merge (if configured)
- [ ] All test failures documented with clear error messages
- [ ] Tests: `test_ci_cd.py` (optional) validates workflow integrity
- [ ] Evidence: Screenshots of passing CI/CD run, coverage report

## Job Assignments (E01)

| Deliverable | Assigned JD | Lead Engineer |
|-------------|------------|---------------|
| D01.1 | DEV-024 (Deliverables Manager) | TBD – guides overall structure, gating |
| D01.2 | DEV-009 (Backend Engineer) | TBD – Ollama client integration |
| D01.3 | AGENT-004 (Agent Observability Lead) | TBD – telemetry design & implementation |
| D01.4 | AGENT-002 (Prompt Systems Engineer) | TBD – schema design for evidence |
| D01.5 | DEV-003 (Database Developer) | TBD – data types, ORM, validation |
| D01.6 | DEV-015 (DevOps/CI-CD Engineer) | TBD – GitHub Actions setup |

## Success Criteria (E01 Exit Gate)
- [ ] All 6 deliverables complete
- [ ] All requirements have passing tests + DoD evidence
- [ ] Code coverage ≥80%
- [ ] New engineer can onboard in <30 minutes
- [ ] Ollama inference works reliably
- [ ] All traces visible and queryable
- [ ] Schema validation prevents invalid data

## Timeline Estimate
**2–3 weeks** (depending on team size and parallelization)

## Blockers / Risks
1. **PostgreSQL setup** – If local install is complex, may increase onboarding time
2. **Ollama model size** – Mixtral 8x7b requires GPU with ~24GB VRAM
3. **Trace storage** – Local OTLP collector setup may require learning curve

## Next Step (Post-E01)
Once E01 exits, E02 (Ingestion Library) becomes unblocked. Ingestion engineers can begin building document import workflows knowing the foundational infrastructure is solid.

---

**Prepared by:** Senior Technical Lead  
**Status:** Awaiting team assignment and kickoff approval  
**Created:** 2026-01-13
