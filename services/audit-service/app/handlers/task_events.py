# [Task]: T060 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""Handler for task events consumed from Redpanda via Dapr Pub/Sub."""
import json
import logging
from datetime import datetime

from app.config import get_db

logger = logging.getLogger(__name__)


async def handle_task_event(event_data: dict) -> dict:
    """
    Process a task event and write it to the audit_logs table.

    Args:
        event_data: The CloudEvent data payload containing task event fields.

    Returns:
        dict with status "ok" on success.
    """
    event_id = event_data.get("event_id", "unknown")
    event_type = event_data.get("event_type", "unknown")
    user_id = event_data.get("user_id")
    task_id = event_data.get("task_id")
    task_data = event_data.get("task_data")
    raw_ts = event_data.get("timestamp")
    if isinstance(raw_ts, str):
        timestamp = datetime.fromisoformat(raw_ts)
    else:
        timestamp = raw_ts or datetime.utcnow()

    logger.info("Processing %s event: %s for task %s", event_type, event_id, task_id)

    conn = None
    try:
        conn = await get_db()
        await conn.execute(
            """INSERT INTO audit_logs (event_id, event_type, user_id, task_id, data, timestamp)
               VALUES ($1, $2, $3, $4, $5::jsonb, $6::timestamptz)
               ON CONFLICT (event_id) DO NOTHING""",
            event_id,
            event_type,
            user_id,
            task_id,
            json.dumps(task_data) if task_data else None,
            timestamp,
        )
        logger.info("Logged %s event: %s", event_type, event_id)
    except Exception as e:
        logger.error("Failed to log event %s: %s", event_id, str(e))
        raise
    finally:
        if conn:
            await conn.close()

    return {"status": "ok"}
