# [Task]: T011, T012 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Database connection and session management for Phase 2 backend.
Uses asyncpg with connection pooling for optimal performance.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from .config import settings


# Create async engine with connection pooling
# Per research.md: pool_size=10, max_overflow=20, pool_pre_ping=True
engine = create_async_engine(
    settings.database_url,
    echo=not settings.is_production,  # Log SQL in development
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Verify connection health before using
)

# Create async session maker with expire_on_commit=False
# This prevents objects from expiring after commit, allowing access to attributes
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """
    Dependency for FastAPI routes to get database session.

    Yields:
        AsyncSession: Database session for the request

    Example:
        @app.get("/users")
        async def get_users(session: AsyncSession = Depends(get_session)):
            ...
    """
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    """
    Create all database tables based on SQLModel models.
    Called during application startup if tables don't exist.

    Note: In production, use Alembic migrations instead.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db_connection():
    """
    Close database connection pool.
    Called during application shutdown.
    """
    await engine.dispose()


# Alias for compatibility with routes
get_async_session = get_session
