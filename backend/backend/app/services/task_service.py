# [Task]: T059-T061, T072, T074, T081-T082, T101 [US2, US3, US4, US6] | [Spec]: specs/002-phase-02-web-app/spec.md
# [Task]: Phase 5 - Added priority and tags support
"""
Task service layer for task management.
Handles business logic for task CRUD operations including priority and tags.
"""
from typing import Optional, List
from datetime import datetime, timedelta
from sqlmodel import select, func, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.task import Task
from app.models.tag import Tag
from app.models.task_tag import TaskTag
from app.schemas.task import TaskCreate, TaskUpdate


def _calculate_next_due_date(current_due: Optional[datetime], pattern: str) -> datetime:
    """Calculate the next due date based on recurrence pattern."""
    base = current_due if current_due else datetime.utcnow()
    if pattern == "daily":
        return base + timedelta(days=1)
    elif pattern == "weekly":
        return base + timedelta(weeks=1)
    elif pattern == "monthly":
        # Advance by one month, handling month-end edge cases
        month = base.month % 12 + 1
        year = base.year + (1 if base.month == 12 else 0)
        day = min(base.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                              31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return base.replace(year=year, month=month, day=day)
    return base + timedelta(days=1)


async def _create_next_recurring_task(session: AsyncSession, completed_task) -> Optional["Task"]:
    """Auto-create the next instance of a recurring task after completion."""
    if not completed_task.recurrence_pattern:
        return None

    next_due = _calculate_next_due_date(completed_task.due_date, completed_task.recurrence_pattern)

    new_task = Task(
        user_id=completed_task.user_id,
        title=completed_task.title,
        description=completed_task.description,
        completed=False,
        priority=completed_task.priority,
        recurrence_pattern=completed_task.recurrence_pattern,
        recurrence_parent_id=completed_task.id,
        due_date=next_due,
    )
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)
    return new_task


async def _sync_task_tags(
    session: AsyncSession,
    task_id: int,
    tag_ids: Optional[List[int]]
) -> None:
    """
    Synchronize task tags by removing old ones and adding new ones.

    Args:
        session: Database session
        task_id: ID of the task
        tag_ids: List of tag IDs to associate (or None to skip)
    """
    if tag_ids is None:
        return

    # Delete existing task_tags for this task
    await session.execute(
        delete(TaskTag).where(TaskTag.task_id == task_id)
    )

    # Add new task_tags
    for tag_id in tag_ids:
        # Verify tag exists
        tag_result = await session.execute(
            select(Tag).where(Tag.id == tag_id)
        )
        if tag_result.scalar_one_or_none():
            task_tag = TaskTag(task_id=task_id, tag_id=tag_id)
            session.add(task_tag)


async def create_task(session: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    """
    Create a new task for a user with priority and tags.

    Args:
        session: Database session
        task_data: Task creation data (title, description, priority, tag_ids)
        user_id: ID of the user creating the task

    Returns:
        Created Task object with tags loaded

    Process:
        1. Validate title is non-empty (handled by TaskCreate schema)
        2. Create Task object with user_id and priority
        3. Save to database
        4. Associate tags via task_tags junction table
        5. Return created task with tags
    """
    # Calculate initial due_date if recurrence is set
    due_date = None
    if task_data.recurrence_pattern:
        due_date = _calculate_next_due_date(None, task_data.recurrence_pattern)

    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=False,
        priority=task_data.priority,
        recurrence_pattern=task_data.recurrence_pattern,
        due_date=due_date,
    )

    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    # Add tags if provided
    if task_data.tag_ids:
        await _sync_task_tags(session, new_task.id, task_data.tag_ids)
        await session.commit()
        await session.refresh(new_task)

    return new_task


async def get_tasks_by_user(session: AsyncSession, user_id: int) -> list[Task]:
    """
    Get all tasks for a specific user, ordered by creation date (newest first).
    Includes related tags via the relationship.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to fetch

    Returns:
        List of Task objects with tags loaded

    Process:
        1. Query tasks WHERE user_id = current_user_id
        2. Order by created_at DESC (newest first)
        3. Return list of tasks (tags auto-loaded via selectin)
    """
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    result = await session.execute(statement)
    tasks = result.scalars().all()

    return list(tasks)


async def get_task_by_id(session: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    """
    Get a specific task by ID, ensuring it belongs to the user.
    Includes related tags via the relationship.

    Args:
        session: Database session
        task_id: ID of the task to fetch
        user_id: ID of the user (for authorization check)

    Returns:
        Task object if found and belongs to user, None otherwise
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await session.execute(statement)
    task = result.scalar_one_or_none()

    return task


async def update_task_status(session: AsyncSession, task_id: int, user_id: int) -> Optional[Task]:
    """
    Toggle the completion status of a task.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for authorization check)

    Returns:
        Updated Task object if found and belongs to user, None otherwise
    """
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Toggle completed status
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)

    # Auto-create next recurring task on completion
    if task.completed:
        await _create_next_recurring_task(session, task)

    return task


async def get_task_statistics(session: AsyncSession, user_id: int) -> dict:
    """
    Get task statistics for a user including priority breakdown.

    Args:
        session: Database session
        user_id: ID of the user

    Returns:
        Dictionary with task statistics:
            - total: Total number of tasks
            - completed: Number of completed tasks
            - incomplete: Number of incomplete tasks
            - completion_percentage: Percentage of completed tasks (0-100)
            - by_priority: Count of tasks by priority
    """
    # Count total tasks
    total_statement = select(func.count(Task.id)).where(Task.user_id == user_id)
    total_result = await session.execute(total_statement)
    total = total_result.scalar() or 0

    # Count completed tasks
    completed_statement = select(func.count(Task.id)).where(
        Task.user_id == user_id,
        Task.completed == True
    )
    completed_result = await session.execute(completed_statement)
    completed = completed_result.scalar() or 0

    # Count by priority
    priority_statement = select(
        Task.priority,
        func.count(Task.id)
    ).where(Task.user_id == user_id).group_by(Task.priority)
    priority_result = await session.execute(priority_statement)
    by_priority = {row[0].value: row[1] for row in priority_result.all()}

    # Calculate incomplete and percentage
    incomplete = total - completed
    completion_percentage = round((completed / total * 100), 1) if total > 0 else 0.0

    return {
        "total": total,
        "completed": completed,
        "incomplete": incomplete,
        "completion_percentage": completion_percentage,
        "by_priority": by_priority,
    }


async def update_task(
    session: AsyncSession,
    task_id: int,
    user_id: int,
    task_data: TaskUpdate
) -> Optional[Task]:
    """
    Update a task's title, description, completion status, priority, and/or tags.

    Args:
        session: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for authorization check)
        task_data: Updated task data

    Returns:
        Updated Task object if found and belongs to user, None otherwise
    """
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        return None

    # Update fields if provided
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.completed is not None:
        task.completed = task_data.completed
    if task_data.priority is not None:
        task.priority = task_data.priority
    if task_data.recurrence_pattern is not None:
        task.recurrence_pattern = task_data.recurrence_pattern
        if task_data.recurrence_pattern and not task.due_date:
            task.due_date = _calculate_next_due_date(None, task_data.recurrence_pattern)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()

    # Sync tags if provided
    if task_data.tag_ids is not None:
        await _sync_task_tags(session, task_id, task_data.tag_ids)
        await session.commit()

    await session.refresh(task)

    return task


async def delete_task(session: AsyncSession, task_id: int, user_id: int) -> bool:
    """
    Delete a task from the database.

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user (for authorization check)

    Returns:
        True if task was deleted, False if not found or doesn't belong to user
    """
    task = await get_task_by_id(session, task_id, user_id)

    if not task:
        return False

    # Delete task (cascade will handle task_tags)
    await session.delete(task)
    await session.commit()

    return True


async def search_tasks(session: AsyncSession, user_id: int, query: str) -> list[Task]:
    """
    Search tasks by title or description using case-insensitive matching.
    Includes related tags via the relationship.

    Args:
        session: Database session
        user_id: ID of the user whose tasks to search
        query: Search query string

    Returns:
        List of Task objects matching the search query
    """
    # Use parameterized queries with ILIKE for case-insensitive search
    search_pattern = f"%{query}%"

    statement = select(Task).where(
        Task.user_id == user_id,
        (Task.title.ilike(search_pattern) | Task.description.ilike(search_pattern))
    ).order_by(Task.created_at.desc())

    result = await session.execute(statement)
    tasks = result.scalars().all()

    return list(tasks)
