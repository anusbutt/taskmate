# [Task]: T009 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Tag SQLModel for database table.
Stores task tags with name and color for categorization.
"""
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

# Import TaskTag here to avoid circular import issues
from app.models.task_tag import TaskTag

if TYPE_CHECKING:
    from app.models.task import Task


class Tag(SQLModel, table=True):
    """
    Tag model for categorizing tasks.

    Attributes:
        id: Primary key, auto-incremented
        name: Tag name (unique, required, 1-50 characters)
        color: Hex color code for UI display (default gray)
        created_at: Tag creation timestamp
        tasks: Many-to-many relationship with Task model
    """

    __tablename__ = "tags"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, index=True)
    color: str = Field(default="#808080", max_length=7)  # Hex color
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="tags",
        link_model=TaskTag,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
