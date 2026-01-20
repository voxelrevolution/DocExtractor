from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    expected_docs: List[Dict[str, Any]] = Field(default_factory=list)
    predicted_docs: List[Dict[str, Any]] = Field(default_factory=list)
    id_key: str = "extraction_id"


class EvaluationResponse(BaseModel):
    documents_scored: int
    mean_field_accuracy: float
    mean_line_item_accuracy: float
