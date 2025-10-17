"""Pydantic schemas for chat endpoints."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(..., description="Latest user utterance")
    location: Optional[str] = Field(None, description="User-provided coarse location")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Client metadata")
