# [Task]: T022 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Rate limiting middleware using slowapi.
Limits API requests to 100 per minute per user per constitution requirement.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

from ..config import settings


def get_user_id_from_request(request: Request) -> str:
    """
    Extract user_id from request state for rate limiting.

    Args:
        request: FastAPI request object

    Returns:
        User ID string if authenticated, IP address otherwise

    Note:
        Uses user_id from request.state (set by auth middleware) if available,
        otherwise falls back to IP address for unauthenticated requests.
    """
    # Try to get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if user_id is not None:
        return f"user:{user_id}"

    # Fall back to IP address for unauthenticated requests
    return get_remote_address(request)


# Initialize limiter with user-based rate limiting
# Per constitution: 100 requests per minute per user
limiter = Limiter(
    key_func=get_user_id_from_request,
    default_limits=[f"{settings.rate_limit_per_minute}/minute"]
)
