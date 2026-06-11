# [Task]: T069 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Audit log API routes.
Provides read-only access to the audit_logs table populated by the audit-service.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session

router = APIRouter(prefix="/api/audit", tags=["Audit"])


@router.get("")
async def get_audit_logs(
    task_id: Optional[int] = Query(None, description="Filter by task ID"),
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    limit: int = Query(50, ge=1, le=200, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_session),
):
    """
    Get audit log entries with optional filtering.

    Returns a list of audit events recorded by the audit-service
    from Redpanda task-events topic.
    """
    query = "SELECT id, event_id, event_type, user_id, task_id, data, timestamp, created_at FROM audit_logs WHERE 1=1"
    params = {}

    if task_id is not None:
        query += " AND task_id = :task_id"
        params["task_id"] = task_id

    if event_type is not None:
        query += " AND event_type = :event_type"
        params["event_type"] = event_type

    query += " ORDER BY id DESC LIMIT :limit OFFSET :offset"
    params["limit"] = limit
    params["offset"] = offset

    result = await session.execute(text(query), params)
    rows = result.fetchall()

    return {
        "count": len(rows),
        "audit_logs": [
            {
                "id": row.id,
                "event_id": row.event_id,
                "event_type": row.event_type,
                "user_id": row.user_id,
                "task_id": row.task_id,
                "data": row.data,
                "timestamp": row.timestamp.isoformat() if row.timestamp else None,
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in rows
        ],
    }
