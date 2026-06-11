# [Task]: T042 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Event publishing module for Dapr Pub/Sub integration.
Publishes task lifecycle events to Redpanda via Dapr sidecar.
"""
from app.events.publisher import EventPublisher

__all__ = ["EventPublisher"]
