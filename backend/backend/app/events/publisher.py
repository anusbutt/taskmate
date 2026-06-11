# [Task]: T043 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Event publisher service for Dapr Pub/Sub.
Publishes task lifecycle events (created, updated, deleted, completed)
to Redpanda via the Dapr sidecar. Fire-and-forget pattern - failures
are logged but never block the API response.
"""
import logging
import os
import uuid
from datetime import datetime
from typing import Optional

from app.schemas.event import EventType, TaskEvent, TaskEventData

logger = logging.getLogger(__name__)

PUBSUB_NAME = "task-pubsub"
TOPIC_NAME = "task-events"

# Check if Dapr is enabled via environment variable
DAPR_ENABLED = os.environ.get("DAPR_ENABLED", "false").lower() == "true"


class EventPublisher:
    """Publishes task events to Redpanda via Dapr Pub/Sub."""

    @staticmethod
    async def publish_task_event(
        event_type: EventType,
        user_id: int,
        task_id: int,
        task: Optional[object] = None,
    ) -> None:
        """
        Publish a task event to Redpanda via Dapr.

        This is fire-and-forget: if the Dapr sidecar is unavailable
        (e.g., local dev without Dapr), the error is logged and
        the API response is NOT blocked.

        Args:
            event_type: Type of event (created, updated, deleted, completed)
            user_id: ID of the user who triggered the event
            task_id: ID of the affected task
            task: Optional Task object to build event data from
        """
        # Skip if Dapr is not enabled - instant return, no blocking
        if not DAPR_ENABLED:
            logger.debug(
                "Dapr disabled, skipping %s event for task %d",
                event_type.value,
                task_id,
            )
            return

        # Wrap ENTIRE operation in try-except for true fire-and-forget
        try:
            # Build task data inside try-except to ensure errors are caught
            task_data = None
            if task is not None:
                task_data = EventPublisher.build_task_data(task)

            event = TaskEvent(
                event_id=f"evt_{uuid.uuid4().hex[:12]}",
                event_type=event_type,
                timestamp=datetime.utcnow(),
                user_id=user_id,
                task_id=task_id,
                task_data=task_data,
            )

            from dapr.clients import DaprClient

            with DaprClient() as client:
                client.publish_event(
                    pubsub_name=PUBSUB_NAME,
                    topic_name=TOPIC_NAME,
                    data=event.model_dump_json(),
                    data_content_type="application/json",
                )
            logger.info(
                "Published %s event: %s for task %d",
                event_type.value,
                event.event_id,
                task_id,
            )
        except Exception as e:
            # Fire-and-forget: log error but don't block API response
            logger.warning(
                "Failed to publish %s event for task %d: %s",
                event_type.value,
                task_id,
                str(e),
            )

    @staticmethod
    def build_task_data(task) -> TaskEventData:
        """
        Build TaskEventData from a Task model instance.

        Args:
            task: Task SQLModel instance

        Returns:
            TaskEventData with current task state snapshot
        """
        # Safely extract tags - handle both loaded and unloaded cases
        tags = []
        try:
            if hasattr(task, "tags") and task.tags:
                tags = [tag.name for tag in task.tags]
        except Exception:
            # If tags relationship fails to load, just use empty list
            pass

        # Safely extract priority
        priority = "P2"  # Default
        try:
            priority = task.priority.value if hasattr(task.priority, "value") else str(task.priority)
        except Exception:
            pass

        return TaskEventData(
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=priority,
            tags=tags,
        )
