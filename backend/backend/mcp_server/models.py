# [Task]: T094 [US9] | Task model for bundled MCP server
"""
Task model for MCP Server database operations.
Mirrors the backend Task model for use in MCP tools.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task model for MCP Server database operations."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: str = Field(default="P2", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Recurrence fields (US11)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=10)
    recurrence_parent_id: Optional[int] = Field(default=None)
    due_date: Optional[datetime] = Field(default=None)
