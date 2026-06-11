# [Task]: T096 [US9] | Database connection for bundled MCP server
"""Database connection for MCP Server (stdio transport)."""
import os
import sys
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Read DATABASE_URL from environment (same as backend)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://localhost/todo_db")

# Ensure the URL uses the asyncpg driver
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

logger.info(f"MCP DB connecting to: {DATABASE_URL[:30]}...")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
