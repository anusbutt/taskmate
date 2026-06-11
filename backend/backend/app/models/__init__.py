# [Task]: T009 | Backend models barrel export
# [Task]: T012 | [Spec]: specs/005-phase-05-cloud-native/spec.md - Added Phase 5 models
"""Backend SQLModel models."""

# Import order matters for relationships
from app.models.user import User
from app.models.task_tag import TaskTag  # Must be before Task and Tag
from app.models.task import Task, Priority
from app.models.tag import Tag
from app.models.audit_log import AuditLog
from app.models.conversation import Conversation
from app.models.message import Message

__all__ = [
    "User",
    "Task",
    "Priority",
    "Tag",
    "TaskTag",
    "AuditLog",
    "Conversation",
    "Message",
]
