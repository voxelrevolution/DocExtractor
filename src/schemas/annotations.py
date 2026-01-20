from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class CorrectionInput(BaseModel):
    extraction_id: Optional[str] = Field(
        None, description="Client-provided extraction identifier"
    )
    field_name: str
    original_value: Optional[str] = None
    corrected_value: str
    feedback_type: Literal["correction", "confirmation", "error"] = "correction"
    user_notes: Optional[str] = None


class CorrectionRecord(CorrectionInput):
    id: int
    created_at: datetime
