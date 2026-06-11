# [Task]: T024 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Health check endpoint for monitoring and load balancing.
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Status message indicating service health

    Example:
        GET /health
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}
