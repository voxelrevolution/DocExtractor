from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from src.schemas.benchmark import BenchmarkManifest


def load_manifest(path: str) -> BenchmarkManifest:
    data = json.loads(Path(path).read_text())
    return BenchmarkManifest.model_validate(data)


def manifest_to_dict(manifest: BenchmarkManifest) -> Dict[str, Any]:
    return manifest.model_dump()
