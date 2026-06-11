# [Task]: T095 [US9] | MCP tools for bundled stdio transport
"""
MCP Tools for task management - consolidated from phase-03/mcp-servers/tools/.
All 5 tools: add_task, list_tasks, complete_task, delete_task, update_task.
"""
from datetime import datetime, timedelta
from typing import Any, Optional

from sqlmodel import select

from mcp_server.database import async_session
from mcp_server.models import Task

VALID_PRIORITIES = {"P1", "P2", "P3"}
VALID_RECURRENCE = {"daily", "weekly", "monthly"}


def _calculate_next_due(base: Optional[datetime], pattern: str) -> datetime:
    """Calculate next due date from base (or now) given a recurrence pattern."""
    base = base or datetime.utcnow()
    if pattern == "daily":
        return base + timedelta(days=1)
    elif pattern == "weekly":
        return base + timedelta(weeks=1)
    elif pattern == "monthly":
        month = base.month % 12 + 1
        year = base.year + (1 if base.month == 12 else 0)
        day = min(base.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                              31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return base.replace(year=year, month=month, day=day)
    return base + timedelta(days=1)


async def add_task(
    user_id: int,
    title: str,
    description: str | None = None,
    priority: str | None = None,
    recurrence_pattern: str | None = None,
) -> dict[str, Any]:
    """Add a new task to the user's task list."""
    if not title or not title.strip():
        return {"success": False, "error": "Title cannot be empty"}

    title = title.strip()
    if len(title) > 255:
        return {"success": False, "error": "Title cannot exceed 255 characters"}

    if description:
        description = description.strip()
        if len(description) > 1000:
            return {"success": False, "error": "Description cannot exceed 1000 characters"}

    if priority:
        priority = priority.upper().strip()
        if priority not in VALID_PRIORITIES:
            return {"success": False, "error": f"Invalid priority '{priority}'. Use P1, P2, or P3"}
    else:
        priority = "P2"

    if recurrence_pattern:
        recurrence_pattern = recurrence_pattern.lower().strip()
        if recurrence_pattern not in VALID_RECURRENCE:
            return {"success": False, "error": f"Invalid recurrence '{recurrence_pattern}'. Use daily, weekly, or monthly"}

    # Calculate initial due_date if recurrence is set
    due_date = _calculate_next_due(None, recurrence_pattern) if recurrence_pattern else None

    try:
        async with async_session() as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description if description else None,
                completed=False,
                priority=priority,
                recurrence_pattern=recurrence_pattern if recurrence_pattern else None,
                due_date=due_date,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "recurrence_pattern": task.recurrence_pattern,
                    "due_date": task.due_date.isoformat() + "Z" if task.due_date else None,
                    "created_at": task.created_at.isoformat() + "Z",
                },
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to create task: {str(e)}"}


async def list_tasks(
    user_id: int,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
) -> dict[str, Any]:
    """Get all tasks for the user, optionally filtered by status and priority."""
    try:
        async with async_session() as session:
            query = select(Task).where(Task.user_id == user_id)
            if completed is not None:
                query = query.where(Task.completed == completed)
            if priority:
                priority = priority.upper().strip()
                if priority in VALID_PRIORITIES:
                    query = query.where(Task.priority == priority)
            query = query.order_by(Task.created_at.desc())
            result = await session.execute(query)
            tasks = result.scalars().all()
            return {
                "success": True,
                "tasks": [
                    {
                        "id": t.id,
                        "title": t.title,
                        "description": t.description,
                        "completed": t.completed,
                        "priority": t.priority,
                        "recurrence_pattern": t.recurrence_pattern,
                        "due_date": t.due_date.isoformat() + "Z" if t.due_date else None,
                        "created_at": t.created_at.isoformat() + "Z" if t.created_at else None,
                    }
                    for t in tasks
                ],
                "count": len(tasks),
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to list tasks: {str(e)}"}


async def complete_task(user_id: int, task_id: int) -> dict[str, Any]:
    """Mark a task as complete."""
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found or doesn't belong to you"}
            task.completed = True
            session.add(task)
            await session.commit()
            await session.refresh(task)

            response = {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                },
                "message": f"Task '{task.title}' marked as complete",
            }

            # Auto-create next recurring task
            if task.recurrence_pattern:
                next_due = _calculate_next_due(task.due_date, task.recurrence_pattern)
                next_task = Task(
                    user_id=task.user_id,
                    title=task.title,
                    description=task.description,
                    completed=False,
                    priority=task.priority,
                    recurrence_pattern=task.recurrence_pattern,
                    recurrence_parent_id=task.id,
                    due_date=next_due,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                )
                session.add(next_task)
                await session.commit()
                await session.refresh(next_task)
                response["next_task"] = {
                    "id": next_task.id,
                    "title": next_task.title,
                    "due_date": next_task.due_date.isoformat() + "Z" if next_task.due_date else None,
                    "recurrence_pattern": next_task.recurrence_pattern,
                }
                response["message"] += f". Next occurrence created (due {next_task.due_date.strftime('%Y-%m-%d') if next_task.due_date else 'N/A'})"

            return response
    except Exception as e:
        return {"success": False, "error": f"Failed to complete task: {str(e)}"}


async def delete_task(user_id: int, task_id: int) -> dict[str, Any]:
    """Delete a task from the user's task list."""
    try:
        async with async_session() as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found or doesn't belong to you"}
            task_info = {"id": task.id, "title": task.title, "completed": task.completed}
            await session.delete(task)
            await session.commit()
            return {
                "success": True,
                "deleted_task": task_info,
                "message": f"Task '{task_info['title']}' has been deleted",
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to delete task: {str(e)}"}


async def update_task(
    user_id: int,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> dict[str, Any]:
    """Update a task's title, description, or priority."""
    if not title and description is None and priority is None:
        return {"success": False, "error": "Please provide a new title, description, or priority to update"}
    if title and len(title.strip()) == 0:
        return {"success": False, "error": "Task title cannot be empty"}
    if title and len(title) > 255:
        return {"success": False, "error": "Task title must be 255 characters or less"}
    if priority:
        priority = priority.upper().strip()
        if priority not in VALID_PRIORITIES:
            return {"success": False, "error": f"Invalid priority '{priority}'. Use P1, P2, or P3"}

    try:
        async with async_session() as session:
            result = await session.execute(
                select(Task).where(Task.id == task_id, Task.user_id == user_id)
            )
            task = result.scalar_one_or_none()
            if not task:
                return {"success": False, "error": f"Task with ID {task_id} not found or doesn't belong to you"}
            if title:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description else None
            if priority:
                task.priority = priority
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return {
                "success": True,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority,
                    "created_at": task.created_at.isoformat() + "Z" if task.created_at else None,
                },
                "message": "Task updated",
            }
    except Exception as e:
        return {"success": False, "error": f"Failed to update task: {str(e)}"}
