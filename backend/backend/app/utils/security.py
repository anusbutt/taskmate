# [Task]: T015, T016, T017, T018 | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Security utilities for authentication and authorization.
Implements password hashing and JWT token management.
"""
from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from ..config import settings

# Password hashing using argon2 (more secure and modern than bcrypt)
ph = PasswordHasher()


def hash_password(password: str) -> str:
    """
    Hash a password using argon2.

    Args:
        password: Plain text password

    Returns:
        Hashed password string

    Example:
        >>> hashed = hash_password("mysecretpassword")
        >>> verify_password("mysecretpassword", hashed)
        True
    """
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches hash, False otherwise

    Example:
        >>> hashed = hash_password("correct_password")
        >>> verify_password("correct_password", hashed)
        True
        >>> verify_password("wrong_password", hashed)
        False
    """
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with optional custom expiration.

    Args:
        data: Payload data to encode in the token (typically {"sub": user_id})
        expires_delta: Optional custom expiration time. Defaults to 7 days per spec.

    Returns:
        Encoded JWT token string

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        '123'
    """
    to_encode = data.copy()

    # Set expiration time (default 7 days per spec)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.jwt_expiration_days)

    to_encode.update({"exp": expire})

    # Encode JWT token with HS256 algorithm per spec
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded payload dict if valid, None if invalid or expired

    Raises:
        JWTError: If token is invalid, expired, or malformed

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        '123'
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


def extract_user_id(token: str) -> Optional[int]:
    """
    Extract user_id from JWT token payload.

    Args:
        token: JWT token string

    Returns:
        User ID as integer if token is valid and contains "sub" claim, None otherwise

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> extract_user_id(token)
        123
    """
    payload = decode_access_token(token)
    if payload is None:
        return None

    user_id_str = payload.get("sub")
    if user_id_str is None:
        return None

    try:
        return int(user_id_str)
    except (ValueError, TypeError):
        return None
