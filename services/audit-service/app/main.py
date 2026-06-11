# [Task]: T061 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Audit Service main application.
FastAPI app with Dapr Pub/Sub subscription to task-events topic.
Receives events from Redpanda and writes them to the audit_logs table.
"""
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.handlers.task_events import handle_task_event
from app.config import get_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create audit_logs table on startup if it doesn't exist."""
    conn = None
    try:
        conn = await get_db()
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id SERIAL PRIMARY KEY,
                event_id VARCHAR(255) UNIQUE NOT NULL,
                event_type VARCHAR(50) NOT NULL,
                user_id VARCHAR(255),
                task_id INTEGER,
                data JSONB,
                timestamp TIMESTAMPTZ DEFAULT NOW(),
                created_at TIMESTAMPTZ DEFAULT NOW()
            )
        """)
        logger.info("audit_logs table ready")
    except Exception as e:
        logger.error("Failed to create audit_logs table: %s", str(e))
    finally:
        if conn:
            await conn.close()
    yield


app = FastAPI(title="Audit Service", version="0.1.0", lifespan=lifespan)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "audit-service"}


# Dapr subscription endpoint - tells Dapr what topics to subscribe to
@app.get("/dapr/subscribe")
async def subscribe():
    """Return Dapr subscription configuration (programmatic)."""
    return [
        {
            "pubsubname": "task-pubsub",
            "topic": "task-events",
            "route": "/events/task-events",
        }
    ]


@app.post("/events/task-events")
async def task_events_handler(request_body: dict):
    """
    Receive task events from Dapr Pub/Sub.
    Dapr sends CloudEvents wrapping the original event payload.
    """
    try:
        # Dapr wraps the payload in a CloudEvent; the actual data is in 'data'
        event_data = request_body.get("data", request_body)

        # If the data is a string (JSON-encoded), parse it
        if isinstance(event_data, str):
            import json
            event_data = json.loads(event_data)

        result = await handle_task_event(event_data)
        return result
    except Exception as e:
        logger.error("Error handling task event: %s", str(e))
        # Return success to Dapr to avoid redelivery on permanent failures
        return {"status": "error", "message": str(e)}
