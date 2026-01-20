from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def load_json_records(path: str) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text())
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        records = data.get("records")
        if isinstance(records, list):
            return records
    raise ValueError("Expected a JSON list or an object with 'records' list.")
