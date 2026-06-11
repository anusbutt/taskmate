# [Task]: T040-T041 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
User service layer for authentication and user management.
Handles business logic for user creation and authentication.
"""
from typing import Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password


async def create_user(session: AsyncSession, user_data: UserCreate) -> Optional[User]:
    """
    Create a new user in the database.

    Args:
        session: Database session
        user_data: User creation data (email, name, password)

    Returns:
        Created User object or None if email already exists

    Process:
        1. Check if email already exists
        2. Hash the password
        3. Create User object
        4. Save to database
        5. Return created user
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    result = await session.execute(statement)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        return None  # Email already in use

    # Hash password and create user
    password_hash = hash_password(user_data.password)

    new_user = User(
        email=user_data.email,
        name=user_data.name,
        password_hash=password_hash
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        session: Database session
        email: User's email address
        password: Plain text password to verify

    Returns:
        User object if authentication succeeds, None otherwise

    Process:
        1. Find user by email
        2. Verify password hash
        3. Return user if valid, None otherwise
    """
    # Find user by email
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        return None  # User not found

    # Verify password
    if not verify_password(password, user.password_hash):
        return None  # Invalid password

    return user
