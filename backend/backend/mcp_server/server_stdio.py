# [Task]: T097 [US9] | MCP server stdio entrypoint
"""
MCP Server stdio entrypoint for subprocess-based transport.
Registers all 5 task management tools and communicates via stdin/stdout.
Used by MCPServerStdio in chat_service.py.
"""
import sys
import os
import json
import logging

# Ensure the backend root is on the path so mcp_server package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from mcp_server.tools import add_task, list_tasks, complete_task, delete_task, update_task

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

server = Server("task-management-mcp")


@server.list_tools()
async def handle_list_tools():
    """List available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Add a new task to the user's task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The authenticated user's ID"},
                    "title": {"type": "string", "description": "The task title (required)", "maxLength": 255},
                    "description": {"type": "string", "description": "Optional task description", "maxLength": 1000},
                    "priority": {"type": "string", "description": "Priority level: P1 (High), P2 (Medium), P3 (Low). Default: P2"},
                    "recurrence_pattern": {"type": "string", "description": "Recurrence: 'daily', 'weekly', or 'monthly'. Omit for one-time tasks.", "enum": ["daily", "weekly", "monthly"]},
                },
                "required": ["user_id", "title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="Get all tasks for the user, optionally filtered by status",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The authenticated user's ID"},
                    "completed": {"type": "boolean", "description": "Filter by completion status (optional)"},
                    "priority": {"type": "string", "description": "Filter by priority P1/P2/P3 (optional)"},
                },
                "required": ["user_id"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The authenticated user's ID"},
                    "task_id": {"type": "integer", "description": "The ID of the task to mark as complete"},
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the user's task list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The authenticated user's ID"},
                    "task_id": {"type": "integer", "description": "The ID of the task to delete"},
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="update_task",
            description="Update a task's title, description, or priority",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The authenticated user's ID"},
                    "task_id": {"type": "integer", "description": "The ID of the task to update"},
                    "title": {"type": "string", "description": "New title for the task (optional)", "maxLength": 255},
                    "description": {"type": "string", "description": "New description (optional)", "maxLength": 1000},
                    "priority": {"type": "string", "description": "New priority P1/P2/P3 (optional)"},
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict):
    """Handle tool calls by dispatching to the appropriate function."""
    tool_map = {
        "add_task": lambda args: add_task(
            user_id=args["user_id"],
            title=args["title"],
            description=args.get("description"),
            priority=args.get("priority"),
            recurrence_pattern=args.get("recurrence_pattern"),
        ),
        "list_tasks": lambda args: list_tasks(
            user_id=args["user_id"],
            completed=args.get("completed"),
            priority=args.get("priority"),
        ),
        "complete_task": lambda args: complete_task(
            user_id=args["user_id"],
            task_id=args["task_id"],
        ),
        "delete_task": lambda args: delete_task(
            user_id=args["user_id"],
            task_id=args["task_id"],
        ),
        "update_task": lambda args: update_task(
            user_id=args["user_id"],
            task_id=args["task_id"],
            title=args.get("title"),
            description=args.get("description"),
            priority=args.get("priority"),
        ),
    }

    handler = tool_map.get(name)
    if not handler:
        logger.error(f"Unknown tool: {name}")
        return [TextContent(type="text", text=json.dumps({"success": False, "error": f"Unknown tool: {name}"}))]

    logger.info(f"Calling tool '{name}' with args: {arguments}")
    result = await handler(arguments)
    logger.info(f"Tool '{name}' result: {result}")
    return [TextContent(type="text", text=json.dumps(result))]


async def main():
    """Run the MCP server with stdio transport."""
    logger.info("Starting MCP server (stdio transport)")
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
