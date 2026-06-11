# [Task]: T058 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""Configuration and database connection for the Audit Service."""
import os
import asyncpg

DATABASE_URL = os.environ.get("DATABASE_URL", "")


async def get_db() -> asyncpg.Connection:
    """Get a database connection."""
    # Parse the DATABASE_URL for asyncpg (strip the driver prefix)
    url = DATABASE_URL
    if url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql://")
    return await asyncpg.connect(url)
