# [Task]: T008 [P] | [Spec]: specs/003-phase-03-ai-chatbot/data-model.md
"""
Message SQLModel for database table.
Represents a single message in a conversation.
"""
from datetime import datetime
from typing import TYPE_CHECKING, Literal, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class Message(SQLModel, table=True):
    """
    Message model representing a single chat message.

    Attributes:
        id: Primary key (UUID)
        conversation_id: Foreign key to conversations.id (CASCADE DELETE)
        role: Message author role ('user' or 'assistant')
        content: Message content text
        created_at: Message timestamp
    """

    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    role: str = Field(nullable=False)  # 'user' or 'assistant' - validated at DB level
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")
