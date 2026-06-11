# [Task]: T055 [P] [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
# [Task]: T008 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Priority
"""
Task SQLModel for database table.
Stores user tasks with title, description, completion status, and priority.
"""
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Priority(str, Enum):
    """Task priority levels."""
    P1 = "P1"  # High priority
    P2 = "P2"  # Medium priority (default)
    P3 = "P3"  # Low priority


# Import TaskTag here to avoid circular import issues
# This works because TaskTag doesn't import Task
from app.models.task_tag import TaskTag

if TYPE_CHECKING:
    from app.models.tag import Tag


class Task(SQLModel, table=True):
    """
    Task model representing a user's task.

    Attributes:
        id: Primary key, auto-incremented
        user_id: Foreign key to users.id (CASCADE DELETE)
        title: Task title (required, 1-200 characters)
        description: Task description (optional, 0-1000 characters)
        completed: Completion status (default False)
        priority: Task priority (P1=High, P2=Medium, P3=Low)
        created_at: Task creation timestamp
        updated_at: Last modification timestamp
        tags: Many-to-many relationship with Tag model
    """

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", ondelete="CASCADE", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: Priority = Field(default=Priority.P2, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Recurrence fields (US11)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=10, index=True)
    recurrence_parent_id: Optional[int] = Field(default=None, foreign_key="tasks.id", ondelete="SET NULL")
    due_date: Optional[datetime] = Field(default=None)

    # Relationships
    tags: List["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTag,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
