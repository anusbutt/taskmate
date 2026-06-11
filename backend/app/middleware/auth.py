# [Task]: T019 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
JWT authentication middleware for FastAPI.
Validates JWT tokens from httpOnly cookies and attaches user_id to request state.
"""
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

from ..utils.security import extract_user_id


async def auth_middleware(request: Request, call_next):
    """
    Middleware to validate JWT tokens from httpOnly cookies.

    For protected routes, extracts JWT from cookie, validates it,
    and attaches user_id to request.state for downstream use.

    Args:
        request: FastAPI request object
        call_next: Next middleware/route handler in chain

    Returns:
        Response from downstream handler

    Raises:
        HTTPException: 401 if token is missing/invalid for protected routes

    Note:
        Routes starting with /api/auth (login, signup) are public.
        All other /api routes require valid JWT token.
    """
    # Skip OPTIONS requests (CORS preflight)
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response

    # Public routes that don't require authentication
    public_paths = [
        "/",
        "/health",
        "/api/health",
        "/api/auth/signup",
        "/api/auth/login",
        "/docs",
        "/redoc",
        "/openapi.json",
    ]

    # Check if current path is public
    path = request.url.path
    if path in public_paths or path.startswith("/docs") or path.startswith("/openapi"):
        response = await call_next(request)
        return response

    # For protected routes, extract and validate JWT token
    if path.startswith("/api"):
        # Get token from httpOnly cookie
        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Not authenticated",
                    "code": "MISSING_TOKEN"
                }
            )

        # Extract user_id from token
        user_id = extract_user_id(token)

        if user_id is None:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid or expired token",
                    "code": "INVALID_TOKEN"
                }
            )

        # Attach user_id to request state for use in route handlers
        request.state.user_id = user_id

    # Continue to next middleware/route handler
    response = await call_next(request)
    return response
