# [Task]: Phase 5 - Tags CRUD Routes
"""
Tag management API endpoints.
Handles tag creation, listing, retrieval, updating, and deletion.
Tags are global (not per-user).
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.schemas.tag import TagCreate, TagUpdate, TagResponse, TagListResponse
from app.services.tag_service import (
    get_all_tags,
    get_tag_by_id,
    create_tag,
    update_tag,
    delete_tag,
)

router = APIRouter(prefix="/api/tags")


@router.get("", response_model=list[TagResponse])
async def list_tags_endpoint(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all available tags.

    Response:
        - 200: List of TagResponse objects (ordered by name)

    Note:
        Tags are global (not per-user)
    """
    tags = await get_all_tags(session)
    return [TagResponse.model_validate(tag) for tag in tags]


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag_endpoint(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific tag by ID.

    Path Parameters:
        - tag_id: Tag ID

    Response:
        - 200: TagResponse with tag details
        - 404: Tag not found
    """
    tag = await get_tag_by_id(session, tag_id)
    if not tag:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )
    return TagResponse.model_validate(tag)


@router.post("", response_model=TagResponse, status_code=201)
async def create_tag_endpoint(
    tag_data: TagCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new tag.

    Request Body:
        - name: Tag name (1-50 chars, unique)
        - color: Optional hex color code (default #808080)

    Response:
        - 201: TagResponse with created tag details
        - 400: Validation error (name already exists)
    """
    try:
        tag = await create_tag(session, tag_data)
        return TagResponse.model_validate(tag)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag_endpoint(
    tag_id: int,
    tag_data: TagUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a tag's name and/or color.

    Path Parameters:
        - tag_id: Tag ID

    Request Body:
        - name: Optional new name (1-50 chars, unique)
        - color: Optional new hex color code

    Response:
        - 200: TagResponse with updated tag details
        - 404: Tag not found
        - 400: Validation error (name conflicts)
    """
    try:
        tag = await update_tag(session, tag_id, tag_data)
        if not tag:
            raise HTTPException(
                status_code=404,
                detail="Tag not found"
            )
        return TagResponse.model_validate(tag)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag_endpoint(
    tag_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a tag.

    Path Parameters:
        - tag_id: Tag ID

    Response:
        - 204: Tag deleted successfully (no content)
        - 404: Tag not found

    Side Effect:
        Also removes tag from all tasks (cleans task_tags junction)
    """
    success = await delete_tag(session, tag_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Tag not found"
        )
    return None
