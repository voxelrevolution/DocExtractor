from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field


class ChatCitation(BaseModel):
    source: str = Field(..., description="Source document name or identifier")
    page: Optional[int] = Field(None, description="1-based page number if available")
    line: Optional[int] = Field(None, description="1-based line number if available")
    snippet: Optional[str] = Field(None, description="Supporting snippet")


class ChatHistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    scope: Literal["document", "corpus"]
    message: str
    history: list[ChatHistoryMessage] = Field(default_factory=list)
    extraction_id: Optional[str] = Field(
        default=None,
        description="Optional extraction_id to scope document-chat to a specific extracted document",
    )

    client_id: Optional[str] = Field(
        default=None,
        description="Optional client identifier used to scope corpus chat to a subset of documents",
    )
    project_id: Optional[str] = Field(
        default=None,
        description="Optional project identifier used to scope corpus chat to a subset of documents",
    )
    batch_id: Optional[str] = Field(
        default=None,
        description="Optional batch identifier used to scope corpus chat to a subset of documents",
    )


class ChatResponse(BaseModel):
    reply: str
    citations: list[ChatCitation] = Field(default_factory=list)
