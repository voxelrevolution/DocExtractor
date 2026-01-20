"""
src/schemas/__init__.py
Data validation schemas using Pydantic.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from uuid import UUID


class DocumentMetadata(BaseModel):
    """Metadata for an ingested document."""

    id: UUID
    filename: str
    file_hash: str
    document_type: Optional[str] = None
    ingestion_timestamp: datetime
    file_size: int

    model_config = ConfigDict(from_attributes=True)


class EvidencePointer(BaseModel):
    """Pointer to evidence within a document."""

    document_id: UUID
    page_number: Optional[int] = None
    region: Optional[Dict[str, Any]] = Field(
        None, description="Bounding box or region info"
    )
    confidence: float = Field(..., ge=0.0, le=1.0)
    citation: str = Field(..., description="Human-readable citation")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "document_id": "550e8400-e29b-41d4-a716-446655440000",
                "page_number": 1,
                "region": {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.15},
                "confidence": 0.95,
                "citation": "Invoice date found on page 1, top section",
            }
        }
    )


class ExtractionResult(BaseModel):
    """Result of extracting fields from a document."""

    document_id: UUID
    extraction_type: str = Field(..., description="e.g., 'invoice', 'contract'")
    fields: Dict[str, Any]
    evidence_list: List[EvidencePointer]
    timestamp: datetime
    version: str = "1.0"

    model_config = ConfigDict(from_attributes=True)


class Annotation(BaseModel):
    """User correction or feedback on extraction results."""

    extraction_result_id: int
    field_name: str
    original_value: Optional[str] = None
    corrected_value: str
    feedback_type: str = Field(
        ..., description="e.g., 'correction', 'confirmation', 'error'"
    )
    user_notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
