# [Task]: T042-T046 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Authentication API endpoints for user registration and login.
Handles signup, login, logout, and user profile retrieval.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.utils.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/api/auth")


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(
    user_data: UserCreate,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user account.

    Request Body:
        - email: Valid email address (unique)
        - name: User's display name (1-255 chars)
        - password: Password (min 8 chars, letter + number)

    Response:
        - 201: UserResponse with user details (no password_hash)
        - 400: Email already registered

    Side Effect:
        Sets httpOnly cookie with JWT access token (7 day expiration)
    """
    # Create user in database
    user = await create_user(session, user_data)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.jwt_expiration_days)
    )

    # Set httpOnly cookie (cross-origin: SameSite=None requires Secure=True)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=settings.jwt_expiration_days * 24 * 60 * 60  # Convert days to seconds
    )

    return UserResponse.model_validate(user)


@router.post("/login", response_model=UserResponse)
async def login(
    credentials: UserLogin,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Authenticate and login an existing user.

    Request Body:
        - email: User's email address
        - password: User's password

    Response:
        - 200: UserResponse with user details
        - 401: Invalid credentials

    Side Effect:
        Sets httpOnly cookie with JWT access token (7 day expiration)
    """
    # Authenticate user
    user = await authenticate_user(session, credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(days=settings.jwt_expiration_days)
    )

    # Set httpOnly cookie (cross-origin: SameSite=None requires Secure=True)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        path="/",
        max_age=settings.jwt_expiration_days * 24 * 60 * 60
    )

    return UserResponse.model_validate(user)


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Logout current user by clearing the access token cookie.
    T062: Also clears conversation state flag for frontend.

    Response:
        - 200: Success message with clear_conversations flag

    Side Effect:
        Deletes access_token cookie
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="none",
        path="/"
    )

    # T062: Return flag to clear frontend conversation state
    return {
        "message": "Logged out successfully",
        "clear_conversations": True  # Signal frontend to clear chat state
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get the currently authenticated user's profile.

    Headers:
        - Cookie: access_token (JWT token, validated by auth middleware)

    Response:
        - 200: UserResponse with user details
        - 401: Not authenticated (handled by middleware)

    Note:
        User ID is extracted from request.state.user_id (set by auth middleware)
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Fetch user from database
    from app.models.user import User
    from sqlmodel import select

    statement = select(User).where(User.id == user_id)
    result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return UserResponse.model_validate(user)
