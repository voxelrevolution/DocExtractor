# Quick Reference – E01 Work Assignments

Print this and distribute to each engineer.

---

## DEV-024: Deliverables Manager

**Role:** Orchestrate D01.1, oversee E01 quality gate  
**Time:** 40–60 hours (2–3 weeks)  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/DEV-024_Deliverables_Manager.json`

### Your Deliverables
- **D01.1** – Development Environment Setup (LEAD)
- **D01.6** – CI/CD & Test Infrastructure (OVERSIGHT)

### Your Tasks
1. **T01.1.2** – Create `scripts/setup.sh` (bootstrap automation)
2. **T01.1.4** – Create `docs/ONBOARDING.md` (with tech writer)
3. **T01.1.5** – Internal validation test (run setup end-to-end)
4. **T01.1.6** – External validation (oversee non-author test)

### DoD Checklist
See: `roadmap/R01.../epics/E01_.../deliverables/D01.1/requirements/R01.1/DoD.md`

### Success = All of These
- [ ] Setup script is idempotent and <30 min
- [ ] Onboarding docs are clear to a newcomer
- [ ] External validation passes
- [ ] All evidence artifacts in `evidence/T01.1.*/`

---

## DEV-001: Python/Backend Engineer

**Role:** Python dependencies and backend skeleton  
**Time:** 20–30 hours  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/DEV-001_Backend_Engineer.json`

### Your Deliverables
- **D01.2** – Local Model Runtime (Ollama Integration) – SUPPORT
- **D01.5** – Core Data Types & Interfaces – SUPPORT

### Your Tasks
1. **T01.1.1** – Create `requirements.txt` (pinned dependencies)
2. Support D01.2 (OllamaClient implementation) – see DEV-009
3. Support D01.5 (Pydantic schemas) – see DEV-003

### Acceptance
- [ ] `requirements.txt` has exact version pins
- [ ] `pip install -r requirements.txt` works
- [ ] Evidence: `pip list` output

---

## DEV-003: Database Developer

**Role:** PostgreSQL schema, ORM models, data types  
**Time:** 20–30 hours  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/DEV-003_Database_Developer.json`

### Your Deliverables
- **D01.3** – Observability & Telemetry – SUPPORT
- **D01.5** – Core Data Types & Interfaces (LEAD)

### Your Tasks
1. **T01.1.3** – Create `docker-compose.yml` (PostgreSQL service)
2. **D01.5** – Implement SQLAlchemy ORM models and Pydantic schemas
3. Support D01.3 (database instrumentation)

### Acceptance
- [ ] `docker-compose up -d postgres` works
- [ ] pgvector extension loaded
- [ ] SQLAlchemy models map to Pydantic
- [ ] mypy passes (strict mode)

---

## DEV-009: Backend Engineer

**Role:** Ollama client integration and structured outputs  
**Time:** 15–20 hours  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/DEV-009_Backend_Engineer.json`

### Your Deliverables
- **D01.2** – Local Model Runtime (Ollama Integration) (LEAD)

### Your Tasks
1. Implement `src/llm/OllamaClient` class
2. Load and verify Mixtral 8x7b model
3. Implement inference with JSON schema validation
4. Test token counting

### Acceptance
- [ ] OllamaClient loads Mixtral successfully
- [ ] Infer() returns structured output
- [ ] Token counting tested
- [ ] Latency < 5s for test prompts

---

## AGENT-002: Prompt Systems Engineer

**Role:** Evidence & citation schema design  
**Time:** 15–20 hours  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/AGENT-002_Prompt_Systems_Engineer.json`

### Your Deliverables
- **D01.4** – Evidence & Citation Schema Design (LEAD)

### Your Tasks
1. Define JSON schema for evidence pointers
2. Define extraction result schema
3. Define annotation schema
4. Create Pydantic models and validation tests
5. Document evidence patterns

### Acceptance
- [ ] All 3 schemas defined and validated
- [ ] Round-trip serialization tests pass
- [ ] Example evidence pointers provided
- [ ] API-level validation working

---

## AGENT-004: Agent Observability Lead

**Role:** Telemetry, tracing, observability infrastructure  
**Time:** 20–30 hours  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/AGENT-004_Agent_Observability_Lead.json`

### Your Deliverables
- **D01.3** – Observability & Telemetry Infrastructure (LEAD)

### Your Tasks
1. Initialize OpenTelemetry SDK
2. Configure trace exporters (OTLP or console)
3. Instrument FastAPI middleware
4. Instrument database queries
5. Instrument LLM inference calls
6. Create local Jaeger or equivalent viewer

### Acceptance
- [ ] All API calls traced with correlation IDs
- [ ] Database queries logged with timing
- [ ] LLM calls include prompt, response, latency
- [ ] Traces exportable to JSON

---

## DEV-015: DevOps/CI-CD Engineer

**Role:** GitHub Actions, testing infrastructure  
**Time:** 15–20 hours  
**JD Reference:** `/Setup/fiab/agents/job_descriptions/DEV-015_DevOps_Engineer.json`

### Your Deliverables
- **D01.6** – CI/CD & Test Infrastructure (LEAD)

### Your Tasks
1. Create `.github/workflows/test.yml`
2. Configure pytest with coverage
3. Set up artifact upload
4. Configure linting (ruff) and type checking (mypy)
5. Document testing workflow

### Acceptance
- [ ] Tests run on every push
- [ ] Coverage report generated (target: 80%+)
- [ ] Failures block merge
- [ ] Artifacts stored for inspection

---

## Non-Author Validator (External)

**Role:** Onboarding validation  
**Time:** 2–3 hours  
**Assignment:** TBD (someone NOT involved in setup creation)

### Your Task
1. **T01.1.6** – Follow `docs/ONBOARDING.md` on a fresh machine
2. Run `./scripts/setup.sh` from scratch
3. Report any confusion, errors, or improvements
4. Sign off: "Setup is reproducible"

### Success = You Never Need to Ask Questions

---

## How to Get Started

### For Everyone
1. **Read your JD fully** – Don't skim; understand your role
2. **Read your task documents** – Each task has full acceptance criteria
3. **Check the DoD** – Know what "done" means before you start
4. **Ask for clarification** – If anything is ambiguous, ask immediately

### For Task Owners
1. Clone repo: `git clone <repo>`
2. Follow `docs/ONBOARDING.md` to set up environment
3. Create a branch: `git checkout -b feature/T01.1.X`
4. Implement your task
5. Run tests: `pytest tests/`
6. Commit with evidence
7. Create PR with test results and evidence links

### For Coordination
- **Daily standup:** Report progress against tasks
- **Status dashboard:** Update `PROJECT_STATUS_DASHBOARD.md` daily
- **Blockers:** Flag immediately, don't wait
- **Evidence:** Save all artifacts to `evidence/[Task]/`

---

## Timeline

- **Week 1 (Jan 13–19):** D01.1 core (setup.sh, requirements, docker-compose)
- **Week 1–2 (Jan 13–26):** D01.2–D01.6 in parallel
- **Week 2–3 (Jan 20–Feb 3):** Integration, validation, DoD closure
- **Feb 3:** E01 EXIT GATE (all tests passing, external validation complete)

---

## Quick Links

| Document | Purpose |
|----------|---------|
| [E01_KICKOFF_PACKAGE.md](/Reserved/DocExtractor/roadmap/R01_.../epics/E01_.../E01_KICKOFF_PACKAGE.md) | Full E01 plan |
| [docs/ONBOARDING.md](/Reserved/DocExtractor/docs/ONBOARDING.md) | Getting started |
| [PROJECT_STATUS_DASHBOARD.md](/Reserved/DocExtractor/PROJECT_STATUS_DASHBOARD.md) | Track progress |
| [task documents](/Reserved/DocExtractor/roadmap/R01_.../epics/E01_.../deliverables/.../requirements/.../tasks/) | Individual task specs |

---

## Questions?

Contact: **Senior Technical Lead** (via Slack/email/standup)  
Escalation: **Project Sponsor**

---

**Let's build something great!**
