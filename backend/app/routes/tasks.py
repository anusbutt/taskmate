# [Task]: T062-T063, T073, T075, T083-T084, T102-T103 [US2, US3, US4, US6] | [Spec]: specs/002-phase-02-web-app/spec.md
"""
Task management API endpoints.
Handles task creation, listing, retrieval, status management, updating, deletion, and search.
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_async_session
from app.events.publisher import EventPublisher
from app.schemas.event import EventType
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.services.task_service import (
    create_task,
    get_tasks_by_user,
    get_task_by_id,
    update_task_status,
    get_task_statistics,
    update_task,
    delete_task,
    search_tasks
)

router = APIRouter(prefix="/api/tasks")


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task_endpoint(
    task_data: TaskCreate,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for the authenticated user.

    Request Body:
        - title: Task title (1-200 chars, non-empty)
        - description: Optional task description (0-1000 chars)

    Response:
        - 201: TaskResponse with created task details
        - 401: Not authenticated (handled by auth middleware)
        - 400: Validation error (invalid title/description)

    Side Effect:
        Inserts new task into database with user_id from JWT
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Create task in database
    task = await create_task(session, task_data, user_id)

    # [T044] Publish task.created event (fire-and-forget)
    await EventPublisher.publish_task_event(
        event_type=EventType.CREATED,
        user_id=user_id,
        task_id=task.id,
        task=task,
    )

    return TaskResponse.model_validate(task)


@router.get("", response_model=list[TaskResponse])
async def get_tasks_endpoint(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get all tasks for the authenticated user.

    Query Parameters:
        None

    Response:
        - 200: List of TaskResponse objects (ordered by created_at DESC)
        - 401: Not authenticated (handled by auth middleware)

    Note:
        Returns empty list if user has no tasks
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Fetch all tasks for user
    tasks = await get_tasks_by_user(session, user_id)

    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/search", response_model=list[TaskResponse])
async def search_tasks_endpoint(
    q: str,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Search tasks by title or description using case-insensitive matching.

    Query Parameters:
        - q: Search query string

    Response:
        - 200: List of TaskResponse objects matching the query (ordered by created_at DESC)
        - 401: Not authenticated (handled by auth middleware)

    Note:
        - Returns empty list if no tasks match the query
        - Uses parameterized queries to prevent SQL injection
        - Case-insensitive search (ILIKE)
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Search tasks with SQL injection protection
    tasks = await search_tasks(session, user_id, q)

    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/stats", response_model=dict)
async def get_task_stats_endpoint(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get task statistics for the authenticated user.

    Response:
        - 200: Dictionary with stats:
            - total: Total number of tasks
            - completed: Number of completed tasks
            - incomplete: Number of incomplete tasks
            - completion_percentage: Percentage of completed tasks (0-100)
        - 401: Not authenticated (handled by auth middleware)

    Note:
        Returns all zeros if user has no tasks
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Fetch task statistics
    stats = await get_task_statistics(session, user_id)

    return stats


@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status_endpoint(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a task.

    Path Parameters:
        - task_id: Task ID

    Response:
        - 200: TaskResponse with updated task details
        - 401: Not authenticated (handled by auth middleware)
        - 404: Task not found or doesn't belong to user

    Side Effect:
        Toggles task.completed field and updates task.updated_at
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Update task status (with user authorization check)
    task = await update_task_status(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # [T047] Publish task.completed event (fire-and-forget)
    await EventPublisher.publish_task_event(
        event_type=EventType.COMPLETED,
        user_id=user_id,
        task_id=task_id,
        task=task,
    )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a task's title, description, or completion status.

    Path Parameters:
        - task_id: Task ID

    Request Body:
        - title: Optional updated title (1-200 chars)
        - description: Optional updated description (0-1000 chars)
        - completed: Optional completion status

    Response:
        - 200: TaskResponse with updated task details
        - 401: Not authenticated (handled by auth middleware)
        - 404: Task not found or doesn't belong to user
        - 400: Validation error (invalid title/description)

    Side Effect:
        Updates task fields and updated_at timestamp
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Update task (with user authorization check)
    task = await update_task(session, task_id, user_id, task_data)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # [T045] Publish task.updated event (fire-and-forget)
    await EventPublisher.publish_task_event(
        event_type=EventType.UPDATED,
        user_id=user_id,
        task_id=task_id,
        task=task,
    )

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a task from the database.

    Path Parameters:
        - task_id: Task ID

    Response:
        - 204: Task deleted successfully (no content)
        - 401: Not authenticated (handled by auth middleware)
        - 404: Task not found or doesn't belong to user

    Side Effect:
        Removes task from database
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Delete task (with user authorization check)
    success = await delete_task(session, task_id, user_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    # [T046] Publish task.deleted event (fire-and-forget, no task_data since deleted)
    await EventPublisher.publish_task_event(
        event_type=EventType.DELETED,
        user_id=user_id,
        task_id=task_id,
    )

    return None  # 204 No Content


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task by ID.

    Path Parameters:
        - task_id: Task ID

    Response:
        - 200: TaskResponse with task details
        - 401: Not authenticated (handled by auth middleware)
        - 404: Task not found or doesn't belong to user

    Note:
        Only returns task if it belongs to the authenticated user
    """
    # Get user_id from request state (set by auth middleware)
    user_id = getattr(request.state, "user_id", None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    # Fetch task by ID (with user authorization check)
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)
