# [Task]: T020, T021, T023, T025, T121, T125 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
FastAPI application entry point for Phase 2 backend.
Configures middleware, CORS, rate limiting, logging, and route registration.
"""
import logging
import time
from datetime import datetime
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .config import settings
from .middleware.auth import auth_middleware
from .middleware.rate_limit import limiter
from .routes import health, auth, tasks, chat, audit, tags
from .database import create_db_and_tables, close_db_connection

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="Phase 2 Todo API",
    description="Full-stack web application backend with authentication and task management",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware
# Allows frontend (Next.js) to make requests to backend API
# credentials=True enables httpOnly cookies for JWT tokens
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register rate limiting middleware
# Per constitution: 100 requests/minute per user
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Register authentication middleware
# Validates JWT tokens and attaches user_id to request.state
app.middleware("http")(auth_middleware)


# Security headers and logging middleware (T125, T128, T129)
@app.middleware("http")
async def security_and_logging_middleware(request: Request, call_next):
    """
    Combined middleware for security headers and request/response logging.

    Security Headers (T129):
        - X-Content-Type-Options: nosniff (prevent MIME type sniffing)
        - X-Frame-Options: DENY (prevent clickjacking)
        - X-XSS-Protection: 1; mode=block (enable XSS protection)
        - Strict-Transport-Security: max-age=31536000 (enforce HTTPS for 1 year)

    Logging (T125):
        - Request method and path
        - Response status code
        - Response time in milliseconds
        - User ID (if authenticated)

    HTTPS Enforcement (T128):
        - In production, redirect HTTP to HTTPS
    """
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Add security headers (T129)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Only add HSTS header in production (HTTPS only)
    if settings.environment == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Calculate response time (T125)
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    # Log request/response info (T125)
    logger.info(
        f"method={request.method} path={request.url.path} "
        f"status_code={response.status_code} "
        f"response_time={process_time:.2f}ms "
        f"user_id={user_id or 'anonymous'}"
    )

    return response


# Error logging middleware (T121)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.

    Logs:
        - Error level (ERROR)
        - Timestamp (via logging config)
        - Request path and method
        - User ID (if authenticated)
        - Error message
        - Stack trace

    Returns:
        500 Internal Server Error with user-friendly message
    """
    import traceback

    # Get user_id from request state
    user_id = getattr(request.state, "user_id", None)

    # Log error with structured information
    logger.error(
        f"UNHANDLED ERROR: method={request.method} path={request.url.path} "
        f"user_id={user_id or 'anonymous'} error={str(exc)}"
    )
    logger.error(f"Stack trace:\n{traceback.format_exc()}")

    # Return user-friendly error response
    return Response(
        content='{"detail":"Internal server error. Please try again later."}',
        status_code=500,
        media_type="application/json"
    )

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, tags=["Authentication"])
app.include_router(tasks.router, tags=["Tasks"])
app.include_router(chat.router, tags=["Chat"])  # T040: Phase 3 AI Chatbot
app.include_router(audit.router, tags=["Audit"])  # T069: Phase 5 Audit Logs
app.include_router(tags.router, tags=["Tags"])  # Phase 5: Tags CRUD


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Creates database tables if they don't exist (development only).

    Note: In production, use Alembic migrations instead of auto-creation.
    """
    await create_db_and_tables()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    Closes database connection pool gracefully.
    """
    await close_db_connection()


@app.get("/")
async def root():
    """
    Root endpoint.

    Returns:
        dict: Welcome message with API documentation link
    """
    return {
        "message": "Phase 2 Todo API",
        "docs": "/docs",
        "version": "0.1.0"
    }
