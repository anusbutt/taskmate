# [Task]: T007 [P] | [Spec]: specs/003-phase-03-ai-chatbot/data-model.md
"""
Conversation SQLModel for database table.
Represents a chat session between a user and the AI assistant.
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat session.

    Attributes:
        id: Primary key (UUID)
        user_id: Foreign key to users.id (CASCADE DELETE)
        created_at: Session start timestamp
        updated_at: Last activity timestamp (auto-updated via trigger)
    """

    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
