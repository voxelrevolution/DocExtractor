#!/usr/bin/env python3
"""Governance audit: structure, naming, duplicates.

Usage:
  python scripts/governance_audit.py [root]

Default root: /Reserved/DocExtractor/roadmap
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT_DEFAULT = Path("/Reserved/DocExtractor/roadmap")
DELIVERABLE_PREFIX_RE = re.compile(r"^(D\d+\.\d+)_")
ROLE_TOKEN_RE = re.compile(r"^(?:JD-[A-Z0-9]+|[A-Z]+-\d{3})$")
TASK_FILE_RE = re.compile(r"^T\d+\.\d+\.\d+_(?:JD-[A-Z0-9]+|[A-Z]+-\d{3})_.+\.md$")


def is_allowed_non_task_file(path: Path) -> bool:
    return path.name in {"README.md", ".gitkeep"}


def find_deliverable_dirs(root: Path) -> list[Path]:
    return [p for p in root.rglob("deliverables/*") if p.is_dir()]


def audit_deliverables(deliverable_dirs: list[Path]) -> list[str]:
    issues: list[str] = []
    seen: dict[str, list[Path]] = {}
    for d in deliverable_dirs:
        m = DELIVERABLE_PREFIX_RE.match(d.name)
        if not m:
            continue
        prefix = m.group(1)
        seen.setdefault(prefix, []).append(d)

    for prefix, paths in seen.items():
        if len(paths) > 1:
            joined = ", ".join(str(p) for p in paths)
            issues.append(f"Duplicate deliverable prefix {prefix}: {joined}")

    return issues


def audit_requirements(deliverable_dirs: list[Path]) -> list[str]:
    issues: list[str] = []
    for d in deliverable_dirs:
        req_root = d / "requirements"
        if not req_root.exists():
            continue
        for req_dir in req_root.iterdir():
            if not req_dir.is_dir():
                continue
            requirement_md = req_dir / "requirement.md"
            dod_md = req_dir / "DoD.md"
            if not requirement_md.exists():
                issues.append(f"Missing requirement.md: {req_dir}")
            if not dod_md.exists():
                issues.append(f"Missing DoD.md: {req_dir}")

            tasks_dir = req_dir / "tasks"
            evidence_dir = req_dir / "evidence"
            if not tasks_dir.exists():
                issues.append(f"Missing tasks/ folder: {req_dir}")
            if not evidence_dir.exists():
                issues.append(f"Missing evidence/ folder: {req_dir}")

            if tasks_dir.exists():
                task_files = [p for p in tasks_dir.iterdir() if p.is_file()]
                if not task_files:
                    issues.append(f"Empty tasks/ folder: {tasks_dir}")
                for f in task_files:
                    if is_allowed_non_task_file(f):
                        continue
                    if not TASK_FILE_RE.match(f.name):
                        issues.append(f"Bad task filename: {f}")

            if evidence_dir.exists():
                evidence_files = [p for p in evidence_dir.iterdir() if p.is_file()]
                if not evidence_files:
                    issues.append(f"Empty evidence/ folder: {evidence_dir}")
                for f in evidence_files:
                    if is_allowed_non_task_file(f):
                        continue
                    if f.suffix.lower() != ".md":
                        continue
                    if not TASK_FILE_RE.match(f.name):
                        issues.append(f"Bad evidence filename: {f}")

    return issues


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT_DEFAULT
    if not root.exists():
        print(f"Root not found: {root}")
        return 2

    deliverable_dirs = find_deliverable_dirs(root)
    issues = []
    issues.extend(audit_deliverables(deliverable_dirs))
    issues.extend(audit_requirements(deliverable_dirs))

    if issues:
        print("GOVERNANCE AUDIT FAILED")
        for item in issues:
            print(f"- {item}")
        return 1

    print("GOVERNANCE AUDIT PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
