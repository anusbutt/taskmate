# [Task]: Phase 5 - Tags CRUD Service
"""
Tag service layer for tag management.
Handles business logic for tag CRUD operations.
"""
from typing import Optional, List
from sqlmodel import select, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.tag import Tag
from app.models.task_tag import TaskTag
from app.schemas.tag import TagCreate, TagUpdate


async def get_all_tags(session: AsyncSession) -> List[Tag]:
    """
    Get all tags ordered by name.

    Args:
        session: Database session

    Returns:
        List of Tag objects
    """
    statement = select(Tag).order_by(Tag.name.asc())
    result = await session.execute(statement)
    tags = result.scalars().all()
    return list(tags)


async def get_tag_by_id(session: AsyncSession, tag_id: int) -> Optional[Tag]:
    """
    Get a specific tag by ID.

    Args:
        session: Database session
        tag_id: ID of the tag to fetch

    Returns:
        Tag object if found, None otherwise
    """
    statement = select(Tag).where(Tag.id == tag_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_tag_by_name(session: AsyncSession, name: str) -> Optional[Tag]:
    """
    Get a tag by its name (case-insensitive).

    Args:
        session: Database session
        name: Tag name to search for

    Returns:
        Tag object if found, None otherwise
    """
    statement = select(Tag).where(Tag.name.ilike(name))
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def create_tag(session: AsyncSession, tag_data: TagCreate) -> Tag:
    """
    Create a new tag.

    Args:
        session: Database session
        tag_data: Tag creation data (name, color)

    Returns:
        Created Tag object

    Raises:
        ValueError: If tag name already exists
    """
    # Check if tag name already exists
    existing = await get_tag_by_name(session, tag_data.name)
    if existing:
        raise ValueError(f"Tag with name '{tag_data.name}' already exists")

    new_tag = Tag(
        name=tag_data.name,
        color=tag_data.color or "#808080"
    )

    session.add(new_tag)
    await session.commit()
    await session.refresh(new_tag)

    return new_tag


async def update_tag(
    session: AsyncSession,
    tag_id: int,
    tag_data: TagUpdate
) -> Optional[Tag]:
    """
    Update a tag's name and/or color.

    Args:
        session: Database session
        tag_id: ID of the tag to update
        tag_data: Updated tag data

    Returns:
        Updated Tag object if found, None otherwise

    Raises:
        ValueError: If new name conflicts with existing tag
    """
    tag = await get_tag_by_id(session, tag_id)
    if not tag:
        return None

    # Check name conflict if name is being changed
    if tag_data.name is not None and tag_data.name.lower() != tag.name.lower():
        existing = await get_tag_by_name(session, tag_data.name)
        if existing:
            raise ValueError(f"Tag with name '{tag_data.name}' already exists")
        tag.name = tag_data.name

    if tag_data.color is not None:
        tag.color = tag_data.color

    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return tag


async def delete_tag(session: AsyncSession, tag_id: int) -> bool:
    """
    Delete a tag and clean up task_tags junction entries.

    Args:
        session: Database session
        tag_id: ID of the tag to delete

    Returns:
        True if tag was deleted, False if not found
    """
    tag = await get_tag_by_id(session, tag_id)
    if not tag:
        return False

    # Delete related task_tags entries (cascade should handle this, but be explicit)
    await session.execute(
        delete(TaskTag).where(TaskTag.tag_id == tag_id)
    )

    # Delete the tag
    await session.delete(tag)
    await session.commit()

    return True


async def get_tags_by_ids(session: AsyncSession, tag_ids: List[int]) -> List[Tag]:
    """
    Get multiple tags by their IDs.

    Args:
        session: Database session
        tag_ids: List of tag IDs to fetch

    Returns:
        List of Tag objects (may be fewer than requested if some IDs don't exist)
    """
    if not tag_ids:
        return []

    statement = select(Tag).where(Tag.id.in_(tag_ids))
    result = await session.execute(statement)
    return list(result.scalars().all())
