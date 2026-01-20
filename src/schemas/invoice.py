from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class EvidencePointer(BaseModel):
    source: str = Field(..., description="Source type, e.g. text or pdf")
    page: Optional[int] = Field(None, description="1-based page number if available")
    line: Optional[int] = Field(None, description="1-based line number in extracted text")
    text: Optional[str] = Field(None, description="Supporting text snippet")
    confidence: float = Field(0.0, ge=0.0, le=1.0)


class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    evidence: List[EvidencePointer] = Field(default_factory=list)


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    unit_price: Optional[str] = None
    amount: Optional[str] = None
    evidence: List[EvidencePointer] = Field(default_factory=list)


class InvoiceExtraction(BaseModel):
    extraction_id: Optional[str] = None
    vendor: ExtractedField = Field(default_factory=ExtractedField)
    invoice_number: ExtractedField = Field(default_factory=ExtractedField)
    invoice_date: ExtractedField = Field(default_factory=ExtractedField)
    subtotal: ExtractedField = Field(default_factory=ExtractedField)
    tax: ExtractedField = Field(default_factory=ExtractedField)
    total: ExtractedField = Field(default_factory=ExtractedField)
    line_items: List[LineItem] = Field(default_factory=list)
    raw_text_excerpt: Optional[str] = None
    validation_errors: List[str] = Field(default_factory=list)
    validation_warnings: List[str] = Field(default_factory=list)
    extraction_metadata: Dict[str, Union[str, int, float]] = Field(default_factory=dict)
    review_required: bool = False
    review_reasons: List[str] = Field(default_factory=list)
