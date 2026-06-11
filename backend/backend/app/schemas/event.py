# [Task]: T014 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Pydantic schemas for event-related data structures.
Used for publishing events to Redpanda via Dapr Pub/Sub.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of task events."""
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    COMPLETED = "completed"


class TaskEventData(BaseModel):
    """
    Task data included in events.

    Contains the task state at the time of the event.
    """

    title: str
    description: Optional[str] = None
    completed: bool
    priority: str  # P1, P2, P3
    tags: List[str] = Field(default_factory=list)  # Tag names


class TaskEvent(BaseModel):
    """
    Schema for task events published to Redpanda.

    Follows the event schema defined in spec.md:
    - event_id: Unique identifier (evt_<uuid>)
    - event_type: created | updated | deleted | completed
    - timestamp: ISO 8601 datetime
    - user_id: ID of user who performed the action
    - task_id: ID of affected task
    - task_data: Snapshot of task state
    """

    event_id: str = Field(..., description="Unique event ID (evt_xxx)")
    event_type: EventType = Field(..., description="Type of event")
    timestamp: datetime = Field(..., description="When the event occurred")
    user_id: int = Field(..., description="User who triggered the event")
    task_id: int = Field(..., description="Affected task ID")
    task_data: Optional[TaskEventData] = Field(default=None, description="Task state snapshot")

    class Config:
        use_enum_values = True


class AuditLogResponse(BaseModel):
    """
    Schema for audit log response.

    Used in GET /api/audit endpoint.
    """

    id: int
    event_id: str
    event_type: str
    user_id: int
    task_id: Optional[int]
    data: Optional[Dict[str, Any]]
    timestamp: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """
    Schema for audit log list response.

    Returns array of audit logs with pagination info.
    """

    logs: List[AuditLogResponse]
    total: int
    page: int = 1
    page_size: int = 50

    class Config:
        from_attributes = True
