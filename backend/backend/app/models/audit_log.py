# [Task]: T011 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
AuditLog SQLModel for database table.
Stores audit trail of all task operations for compliance and debugging.
"""
from datetime import datetime
from typing import Any, Dict, Optional

from sqlmodel import Column, Field, SQLModel
from sqlalchemy import JSON


class AuditLog(SQLModel, table=True):
    """
    Audit log model for tracking task operations.

    Attributes:
        id: Primary key, auto-incremented
        event_id: Unique event identifier (e.g., evt_abc123)
        event_type: Type of event (created, updated, deleted, completed)
        user_id: ID of user who performed the action
        task_id: ID of affected task (nullable for deleted tasks)
        data: JSON blob with event payload
        timestamp: When the event occurred
        created_at: When the log entry was created
    """

    __tablename__ = "audit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: str = Field(max_length=50, unique=True, index=True)
    event_type: str = Field(max_length=20, index=True)  # created, updated, deleted, completed
    user_id: int = Field(index=True)
    task_id: Optional[int] = Field(default=None, index=True)
    data: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    timestamp: datetime = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
