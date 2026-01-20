from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ClientRecord(BaseModel):
    client_id: str = Field(..., description="Stable identifier (slug) used for scoping")
    display_name: str = Field(..., description="Human friendly name")
    aliases: list[str] = Field(default_factory=list, description="Alternative names/domains used for matching")


class ClientCreateRequest(BaseModel):
    client_id: str
    display_name: str
    aliases: list[str] = Field(default_factory=list)


class ClientResolution(BaseModel):
    client_id: Optional[str] = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list, description="Human-readable signals used for the guess")
    policy: str = Field(..., description="Resolution policy applied (auto|suggest|unknown)")
