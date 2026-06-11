# [Task]: T037 [US1] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Pydantic schemas for user-related requests and responses.
Provides validation and serialization for API endpoints.
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    """
    Schema for user signup request.

    Validation:
        - email: Must be valid email format (RFC 5322)
        - name: 1-255 characters, non-empty
        - password: Minimum 8 characters with at least one letter and one number
    """

    email: EmailStr = Field(..., max_length=255, description="Valid email address")
    name: str = Field(..., min_length=1, max_length=255, description="User's display name")
    password: str = Field(..., min_length=8, description="Password (min 8 chars, letter + number)")

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password contains at least one letter and one number."""
        has_letter = any(c.isalpha() for c in v)
        has_number = any(c.isdigit() for c in v)

        if not has_letter or not has_number:
            raise ValueError("Password must contain at least one letter and one number")

        return v

    @field_validator("name")
    @classmethod
    def validate_name_not_whitespace(cls, v: str) -> str:
        """Validate name is not only whitespace."""
        if not v.strip():
            raise ValueError("Name cannot be only whitespace")
        return v.strip()


class UserLogin(BaseModel):
    """
    Schema for user login request.

    Validation:
        - email: Must be valid email format
        - password: Required (no minimum length for login)
    """

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """
    Schema for user response (excludes password_hash).

    Used in signup, login, and GET /me responses.
    """

    id: int
    email: str
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow creation from SQLModel instances
