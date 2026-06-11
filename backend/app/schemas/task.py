# [Task]: T056 [US2] | [Spec]: specs/002-phase-02-web-app/spec.md
# [Task]: T015 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added priority and tags
"""
Pydantic schemas for task-related requests and responses.
Provides validation and serialization for task API endpoints.
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from app.models.task import Priority
from app.schemas.tag import TagResponse


class TaskCreate(BaseModel):
    """
    Schema for task creation request.

    Validation:
        - title: 1-200 characters, non-empty
        - description: Optional, 0-1000 characters
        - priority: P1 (High), P2 (Medium), P3 (Low) - default P2
        - tag_ids: Optional list of tag IDs to associate
    """

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    priority: Priority = Field(default=Priority.P2, description="Task priority (P1=High, P2=Medium, P3=Low)")
    tag_ids: Optional[List[int]] = Field(default=None, description="List of tag IDs to associate")
    recurrence_pattern: Optional[str] = Field(default=None, description="Recurrence: 'daily', 'weekly', or 'monthly'")

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, v: str) -> str:
        """Validate title is not only whitespace."""
        if not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip()

    @field_validator("recurrence_pattern")
    @classmethod
    def validate_recurrence_pattern(cls, v: Optional[str]) -> Optional[str]:
        """Validate recurrence pattern is a valid value."""
        if v is not None and v not in ("daily", "weekly", "monthly"):
            raise ValueError("recurrence_pattern must be 'daily', 'weekly', or 'monthly'")
        return v


class TaskUpdate(BaseModel):
    """
    Schema for task update request.

    Allows partial updates (all fields optional).
    """

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = Field(default=None)
    priority: Optional[Priority] = Field(default=None, description="Task priority")
    tag_ids: Optional[List[int]] = Field(default=None, description="List of tag IDs to associate")
    recurrence_pattern: Optional[str] = Field(default=None, description="Recurrence: 'daily', 'weekly', or 'monthly'")

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Validate title is not only whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be only whitespace")
        return v.strip() if v is not None else None

    @field_validator("recurrence_pattern")
    @classmethod
    def validate_recurrence_pattern(cls, v: Optional[str]) -> Optional[str]:
        """Validate recurrence pattern is a valid value."""
        if v is not None and v not in ("daily", "weekly", "monthly"):
            raise ValueError("recurrence_pattern must be 'daily', 'weekly', or 'monthly'")
        return v


class TaskResponse(BaseModel):
    """
    Schema for task response.

    Used in all task endpoint responses.
    """

    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: Priority
    tags: List[TagResponse] = Field(default_factory=list)
    recurrence_pattern: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """
    Schema for task list response.

    Returns array of tasks with metadata.
    """

    tasks: list[TaskResponse]
    total: int

    class Config:
        from_attributes = True


class TaskStatsResponse(BaseModel):
    """
    Schema for task statistics response.
    """

    total: int
    completed: int
    pending: int
    by_priority: dict[str, int] = Field(default_factory=dict)

    class Config:
        from_attributes = True
