# [Task]: T038-T040 [US1] | [Spec]: specs/003-phase-03-ai-chatbot/contracts/chat-api.md
"""
Chat API Route - POST /api/chat endpoint.
Handles natural language task management via AI chatbot.
"""
import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.routes.auth import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """
    T038: POST /api/chat endpoint.
    T039: JWT authentication via get_current_user dependency.

    Send a message to the AI assistant and receive a response.

    Args:
        request: ChatRequest with message and optional conversation_id
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        ChatResponse with AI response, conversation_id, task_updated flag, timestamp

    Raises:
        400: Invalid request (empty message)
        401: Not authenticated
        500: AI service error
    """
    try:
        # Initialize chat service
        chat_service = ChatService(session)

        # Process the message
        result = await chat_service.process_message(
            user_id=current_user.id,
            message=request.message,
            conversation_id=request.conversation_id,
        )

        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            task_updated=result["task_updated"],
            timestamp=result["timestamp"],
        )

    except Exception as e:
        logger.exception(f"Chat endpoint error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "detail": "AI service temporarily unavailable",
                "fallback_message": "Please try using the task list directly.",
            },
        )
