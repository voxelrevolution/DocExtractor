from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ExportRequest(BaseModel):
    extraction_ids: Optional[List[str]] = None
    include_line_items: bool = True
    client_id: Optional[str] = None


class ExportResponse(BaseModel):
    rows: List[Dict[str, str]] = Field(default_factory=list)
