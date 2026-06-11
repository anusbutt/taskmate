# [Task]: T010 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
TaskTag SQLModel for many-to-many relationship between Task and Tag.
Junction table linking tasks to their tags.
"""
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskTag(SQLModel, table=True):
    """
    Junction table for Task-Tag many-to-many relationship.

    Attributes:
        task_id: Foreign key to tasks.id (CASCADE DELETE)
        tag_id: Foreign key to tags.id (CASCADE DELETE)
    """

    __tablename__ = "task_tags"

    task_id: Optional[int] = Field(
        default=None,
        foreign_key="tasks.id",
        primary_key=True,
        ondelete="CASCADE"
    )
    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="tags.id",
        primary_key=True,
        ondelete="CASCADE"
    )
