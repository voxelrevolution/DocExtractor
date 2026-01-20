from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class BenchmarkDocument(BaseModel):
    extraction_id: str
    filename: str
    source_type: str = Field(..., description="digital_pdf or scanned_pdf")
    vendor: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)


class BenchmarkManifest(BaseModel):
    name: str
    version: str
    documents: List[BenchmarkDocument] = Field(default_factory=list)
