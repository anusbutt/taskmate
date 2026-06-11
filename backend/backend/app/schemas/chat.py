# [Task]: T013 [P] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/chat-api.md
"""
Chat API Pydantic schemas for request/response validation.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for POST /api/chat endpoint."""

    message: str = Field(..., min_length=1, max_length=1000, description="User's natural language input")
    conversation_id: Optional[UUID] = Field(
        None, description="Existing conversation ID for context. If omitted, creates new conversation"
    )


class ChatResponse(BaseModel):
    """Response schema for POST /api/chat endpoint."""

    response: str = Field(..., description="AI assistant's response text")
    conversation_id: UUID = Field(..., description="Conversation ID (use for subsequent messages)")
    task_updated: bool = Field(..., description="True if a task was created/modified/deleted")
    timestamp: datetime = Field(..., description="Response timestamp")


class ChatErrorResponse(BaseModel):
    """Error response schema for chat endpoint."""

    detail: str = Field(..., description="Error message")
    fallback_message: Optional[str] = Field(None, description="Suggested alternative action")
