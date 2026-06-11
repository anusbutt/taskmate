# [Task]: T036 [P] [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
User SQLModel for database table.
Stores user account information with secure password hashing.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """
    User model representing an account in the system.

    Attributes:
        id: Primary key, auto-incremented
        email: Unique email address for login
        name: User's display name
        password_hash: Bcrypt-hashed password (never store plain text)
        created_at: Account creation timestamp
        updated_at: Last modification timestamp
    """

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
