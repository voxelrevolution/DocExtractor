# Project Navigation Guide

**Navigate this project by answering the question below. Find your document in seconds.**

---

## "I want to..."

### As a **Sponsor / Business Lead**
| Goal | Where to Go |
|------|------------|
| Get a 5-min overview of any epic | `/roadmap/R01_LocalDocExtractionPlatform/epics/ExX/summaries/EXECUTIVE_SUMMARY.md` |
| Understand project vision & tech stack | `/charter/CHARTER_01_ApplicationScope.md` + `/roadmap/R01_LocalDocExtractionPlatform/roadmap.md` |
| See current project status | `PROJECT_STATUS_DASHBOARD.md` (at root) |
| Approve an epic before kickoff | Read `/epics/ExX/summaries/READY_FOR_KICKOFF.md` |
| Review how tasks map to job descriptions | `/epics/ExX/summaries/TASK_JD_MAPPING.md` |
| Understand governance gates & DoD | `/governance/GOVERNANCE_OVERVIEW.md` |
| Verify epic completion | `/epics/ExX/summaries/FINAL_VERIFICATION.md` |

---

### As a **Project Manager / Tech Lead**
| Goal | Where to Go |
|------|------------|
| Plan a new epic | Read `/charter/CHARTER_04_EpicKickoffTemplate.md`, then create `/epics/ExX/` structure |
| Decompose epic into tasks | See the pattern in `/epics/E01/tasks/` – follow it |
| Assign engineers to tasks | Create/update `/epics/ExX/summaries/TASK_JD_MAPPING.md` with JD rationale |
| Track epic progress | Update `PROJECT_STATUS_DASHBOARD.md` daily; file completed artifacts in `/evidence/` |
| Write requirement specs | Follow pattern in `/epics/E01/requirements/` |
| Understand task naming | `T{Epic}{Deliverable}.{Requirement}.{Task}_{JD-ID}_TaskName.md` |
| Access governance rules | `/governance/GOVERNANCE_OVERVIEW.md` |

---

### As an **Engineer / Developer**
| Goal | Where to Go |
|------|------------|
| Find my task | Look in `/roadmap/R01_LocalDocExtractionPlatform/epics/ExX/tasks/` for file with your JD-ID |
| Understand my role & responsibilities | Read your JD file in `/Setup/fiab/agents/job_descriptions/` (e.g., `DEV-024_Deliverables_Manager.json`) |
| See task requirements & acceptance criteria | Read your task file fully – top section has spec, bottom section has DoD checklist |
| Understand the tech stack | `/roadmap/R01_LocalDocExtractionPlatform/roadmap.md` (locked in E01) |
| Set up dev environment | `/docs/ONBOARDING.md` – 30-minute walkthrough |
| Check current code structure | `/src/` (organized by bounded contexts: api/, database/, llm/, observability/, schemas/) |
| Submit evidence of work | Create a file in `/evidence/ExX_T0X.Y.Z_{yourname}_{date}.md` with links to tests, logs, PRs, etc. |

---

### As an **External Validator / QA**
| Goal | Where to Go |
|------|------------|
| Understand what to test for an epic | `/epics/ExX/summaries/FINAL_VERIFICATION.md` – validation checklist |
| See acceptance criteria for all requirements | `/epics/ExX/requirements/RxX.Y/requirement.md` |
| Review Definition of Done | `/epics/ExX/DoD.md` |
| Access test results & evidence | `/evidence/` directory (linked from task status) |
| Sign off on epic completion | `/epics/ExX/summaries/FINAL_VERIFICATION.md` – add your sign-off when all checks pass |

---

### As a **New Team Member**
| Goal | Where to Go |
|------|------------|
| Understand the project in 10 minutes | `/README.md` (at root) |
| Set up my machine | `/docs/ONBOARDING.md` |
| Understand the governance model | `/governance/GOVERNANCE_OVERVIEW.md` |
| See where all the documents live | **You're reading it!** This file. |
| Find my task & requirements | Ask your project lead for your task file path, then read it top-to-bottom |

---

## Directory Structure at a Glance

```
/Reserved/DocExtractor/
├── README.md                           ← Start here
├── PROJECT_STATUS_DASHBOARD.md         ← Current epic status (sponsors & leads)
├── charter/                            ← Foundational project documents
│   ├── CHARTER_01_ApplicationScope.md
│   ├── CHARTER_02_RoadmapEpics.md
│   ├── CHARTER_03_GovernanceModel.md
│   └── CHARTER_04_EpicKickoffTemplate.md
├── governance/                         ← Governance rules & patterns
│   ├── GOVERNANCE_OVERVIEW.md          ← How governance works
│   └── (templates for docs)
├── roadmap/
│   └── R01_LocalDocExtractionPlatform/
│       ├── roadmap.md                  ← Master epic sequencing
│       └── epics/
│           ├── E01_CoreFoundation/
│           │   ├── epic.md
│           │   ├── summaries/          ← **All epic summary docs live here**
│           │   │   ├── EXECUTIVE_SUMMARY.md
│           │   │   ├── TASK_JD_MAPPING.md
│           │   │   ├── KICKOFF_PACKAGE.md
│           │   │   ├── READY_FOR_KICKOFF.md
│           │   │   ├── TEAM_QUICK_REFERENCE.md
│           │   │   └── FINAL_VERIFICATION.md
│           │   ├── deliverables/       ← Deliverable specs
│           │   ├── requirements/       ← Requirement specs
│           │   ├── tasks/              ← Task specs (T01.1.1_JD-XXX_Name.md)
│           │   └── DoD.md
│           ├── E02–E05/                ← (same structure)
│           └── (future epics)
├── docs/                               ← Project-wide documentation
│   ├── ONBOARDING.md                   ← Setup guide
│   └── (architecture, API, etc.)
├── src/                                ← Python codebase
│   ├── api/
│   ├── database/
│   ├── llm/
│   ├── observability/
│   └── schemas/
├── tests/                              ← Test suite
├── scripts/                            ← Setup & utility scripts
├── evidence/                           ← Artifacts, logs, test results (filed per task)
└── docker-compose.yml                  ← Local dev environment
```

---

## Quick Links by Document Type

### **Epic Planning & Status**
- Master roadmap: [roadmap.md](/roadmap/R01_LocalDocExtractionPlatform/roadmap.md)
- E01 status: [E01 summaries folder](/roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/summaries/)
- E02 status: [E02 summaries folder](/roadmap/R01_LocalDocExtractionPlatform/epics/E02_IngestionLocalLibrary/summaries/)
- Overall dashboard: [PROJECT_STATUS_DASHBOARD.md](/PROJECT_STATUS_DASHBOARD.md)

### **Governance & Patterns**
- Governance overview: [GOVERNANCE_OVERVIEW.md](/governance/GOVERNANCE_OVERVIEW.md)
- Definition of Done: [E01 DoD](/roadmap/R01_LocalDocExtractionPlatform/epics/E01_CoreFoundation/DoD.md)
- Epic template: [CHARTER_04_EpicKickoffTemplate.md](/charter/CHARTER_04_EpicKickoffTemplate.md)

### **Setup & Onboarding**
- Dev setup: [ONBOARDING.md](/docs/ONBOARDING.md)
- Tech stack: [roadmap.md - Tech Stack section](/roadmap/R01_LocalDocExtractionPlatform/roadmap.md)

### **Foundational Documents**
- Project vision: [CHARTER_01_ApplicationScope.md](/charter/CHARTER_01_ApplicationScope.md)
- Roadmap overview: [CHARTER_02_RoadmapEpics.md](/charter/CHARTER_02_RoadmapEpics.md)
- Governance model: [CHARTER_03_GovernanceModel.md](/charter/CHARTER_03_GovernanceModel.md)

---

## How to Contribute to This Guide

If you find a document that isn't in this guide, or a question you had that wasn't answered, **add it**. This is a living document. Update it as the project evolves.

