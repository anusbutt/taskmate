# [Task]: T059 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""AuditLog data class for the Audit Service."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class AuditLog:
    """Audit log entry matching the audit_logs table schema."""
    event_id: str
    event_type: str
    user_id: int
    task_id: Optional[int]
    data: Optional[Dict[str, Any]]
    timestamp: str
    created_at: datetime = field(default_factory=datetime.utcnow)
