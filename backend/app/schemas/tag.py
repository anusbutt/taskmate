# [Task]: T013 | [Spec]: specs/005-phase-05-cloud-native/spec.md
"""
Pydantic schemas for tag-related requests and responses.
Provides validation and serialization for tag API endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class TagCreate(BaseModel):
    """
    Schema for tag creation request.

    Validation:
        - name: 1-50 characters, non-empty
        - color: Valid hex color code (default gray)
    """

    name: str = Field(..., min_length=1, max_length=50, description="Tag name")
    color: Optional[str] = Field(default="#808080", max_length=7, description="Hex color code")

    @field_validator("name")
    @classmethod
    def validate_name_not_whitespace(cls, v: str) -> str:
        """Validate name is not only whitespace."""
        if not v.strip():
            raise ValueError("Tag name cannot be only whitespace")
        return v.strip()

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate color is a valid hex code."""
        if v is None:
            return "#808080"
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code (e.g., #FF5733)")
        return v.upper()


class TagUpdate(BaseModel):
    """
    Schema for tag update request.

    Allows partial updates (all fields optional).
    """

    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    color: Optional[str] = Field(default=None, max_length=7)

    @field_validator("name")
    @classmethod
    def validate_name_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        """Validate name is not only whitespace if provided."""
        if v is not None and not v.strip():
            raise ValueError("Tag name cannot be only whitespace")
        return v.strip() if v is not None else None

    @field_validator("color")
    @classmethod
    def validate_hex_color(cls, v: Optional[str]) -> Optional[str]:
        """Validate color is a valid hex code if provided."""
        if v is None:
            return None
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex code (e.g., #FF5733)")
        return v.upper()


class TagResponse(BaseModel):
    """
    Schema for tag response.

    Used in all tag endpoint responses.
    """

    id: int
    name: str
    color: str
    created_at: datetime

    class Config:
        from_attributes = True


class TagListResponse(BaseModel):
    """
    Schema for tag list response.

    Returns array of tags.
    """

    tags: list[TagResponse]
    total: int

    class Config:
        from_attributes = True
