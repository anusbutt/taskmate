# [Task]: T031-T037, T048, T089, T099 [US1, US2, US8, US9] | [Spec]: specs/003-phase-03-ai-chatbot/plan.md
"""
Chat Service - Orchestrates AI chatbot interactions.
T099: Refactored to use OpenAI Agents SDK with MCP server via stdio transport (subprocess).
Falls back to direct LLM call if MCP subprocess is unavailable.
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.config import settings
from app.models.conversation import Conversation
from app.models.message import Message

logger = logging.getLogger(__name__)

# Path to the bundled MCP server stdio entrypoint
MCP_SERVER_SCRIPT = str(Path(__file__).resolve().parent.parent.parent / "mcp_server" / "server_stdio.py")

# T032, T048: Agent system prompt for task management
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their tasks through natural language.

You have access to MCP tools for task management. The user_id will be provided to you — always pass it to the tools.

When the user wants to:
- Create/add a task: Use add_task with their task title
- View/list/show tasks: Use list_tasks to show their tasks
- Complete/mark done: FIRST call list_tasks to find the task_id, THEN call complete_task
- Delete/remove: FIRST call list_tasks to find the task_id, THEN call delete_task
- Update/change/rename: FIRST call list_tasks to find the task_id, THEN call update_task
- Create recurring task: Use add_task with recurrence_pattern ('daily', 'weekly', or 'monthly')
- When a recurring task is completed, a new instance is auto-created with the next due date

Guidelines:
- Be concise and friendly
- Confirm actions clearly (e.g., "Done! I've added 'buy groceries' to your list.")
- When listing tasks, format them nicely with numbers and status
- If the user's intent is unclear, ask for clarification
- Extract task titles naturally from conversational requests
- Always respond in a helpful, conversational tone
- NEVER output raw function call text. Always use the tools properly.
- When you need a task_id but don't have it, call list_tasks first to look it up.

IMPORTANT:
- The user_id is {user_id}. Always pass this to every tool call.
- You do NOT have access to previous conversation messages. Each message is independent.
- If you need a task_id, always call list_tasks first to find it.
- Detect the user's language. If the user writes in Urdu, respond in Urdu. If in English, respond in English. Always match the user's language."""


class ChatService:
    """Service for handling chat interactions with AI agent."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_conversation(
        self, user_id: int, conversation_id: Optional[UUID] = None
    ) -> Conversation:
        """T035: Get existing conversation or create new one for the user."""
        if conversation_id:
            result = await self.session.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
            )
            conversation = result.scalar_one_or_none()
            if conversation:
                return conversation

        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def save_message(
        self, conversation_id: UUID, role: str, content: str
    ) -> Message:
        """T036: Save a message to the conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_conversation_history(
        self, conversation_id: UUID, limit: int = 20
    ) -> list[Message]:
        """T037: Get recent messages from conversation for context."""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def process_message(
        self,
        user_id: int,
        message: str,
        conversation_id: Optional[UUID] = None,
    ) -> dict:
        """Process a user message and return AI response."""
        from sqlalchemy.exc import OperationalError, InterfaceError

        try:
            conversation = await self.get_or_create_conversation(user_id, conversation_id)
            await self.save_message(conversation.id, "user", message)
            history = await self.get_conversation_history(conversation.id)

            messages = [{"role": msg.role, "content": msg.content} for msg in history]

            # Try MCP-powered agent (stdio subprocess), fall back to direct LLM
            response_text, task_updated = await self._call_agent_with_mcp(user_id, message, messages)

            await self.save_message(conversation.id, "assistant", response_text)

            return {
                "response": response_text,
                "conversation_id": conversation.id,
                "task_updated": task_updated,
                "timestamp": datetime.utcnow(),
            }

        except (OperationalError, InterfaceError) as e:
            logger.error(f"Database connection error: {e}")
            return {
                "response": "I'm having trouble connecting to the task service right now. Please try again in a moment.",
                "conversation_id": conversation_id,
                "task_updated": False,
                "timestamp": datetime.utcnow(),
                "error": "service_unavailable",
            }
        except Exception as e:
            logger.exception(f"Error processing chat message: {e}")
            raise

    async def _call_agent_with_mcp(
        self, user_id: int, message: str, history: list[dict]
    ) -> tuple[str, bool]:
        """
        T099: Call AI agent with MCP server via stdio transport.
        The Agents SDK spawns the MCP server as a subprocess,
        discovers tools via stdin/stdout, and lets the LLM decide which to call.
        """
        from agents import Agent, Runner
        from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
        from agents.mcp import MCPServerStdio
        from openai import AsyncOpenAI

        # Pass DATABASE_URL explicitly to subprocess — the env var may use
        # a different name or format in the parent process
        import os
        subprocess_env = os.environ.copy()
        subprocess_env["DATABASE_URL"] = settings.database_url

        mcp_server = MCPServerStdio(
            params={
                "command": sys.executable,
                "args": [MCP_SERVER_SCRIPT],
                "env": subprocess_env,
            },
            cache_tools_list=True,
            name="task-management-mcp",
            client_session_timeout_seconds=30,
        )

        try:
            async with mcp_server:
                external_client = AsyncOpenAI(
                    api_key=settings.llm_api_key,
                    base_url=settings.llm_base_url,
                    timeout=30.0,
                )

                llm_model = OpenAIChatCompletionsModel(
                    model=settings.llm_model,
                    openai_client=external_client,
                )

                agent = Agent(
                    name="TaskAssistant",
                    model=llm_model,
                    instructions=SYSTEM_PROMPT.format(user_id=user_id),
                    mcp_servers=[mcp_server],
                )

                # Send only the current user message to avoid stale history
                # contaminating the LLM. MCP tools are stateless (user_id in every call).
                input_messages = [{"role": "user", "content": message}]
                result = await Runner.run(agent, input=input_messages)

                response_text = result.final_output or "I'm not sure how to help with that."

                task_updated = False
                for item in result.new_items:
                    if hasattr(item, 'type') and item.type == 'tool_call_item':
                        task_updated = True
                        break

                return response_text, task_updated

        except Exception as e:
            logger.warning(f"MCP agent failed, falling back to direct LLM: {e}")
            return await self._call_llm_direct(user_id, message, history)

    async def _call_llm_direct(
        self, user_id: int, message: str, history: list[dict]
    ) -> tuple[str, bool]:
        """
        Fallback: Direct LLM API call without MCP tools.
        Used when MCP subprocess is unavailable.
        """
        import asyncio
        from openai import AsyncOpenAI
        from httpx import TimeoutException

        try:
            client = AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url,
                timeout=30.0,
            )

            api_messages = [{"role": "system", "content": SYSTEM_PROMPT.format(user_id=user_id)}]
            api_messages.extend(history[-10:])

            response = await client.chat.completions.create(
                model=settings.llm_model,
                messages=api_messages,
            )

            return response.choices[0].message.content or "I'm not sure how to help with that.", False

        except asyncio.TimeoutError:
            logger.warning("LLM API call timed out")
            return "I'm taking longer than expected to respond. Please try again in a moment.", False
        except TimeoutException:
            logger.warning("LLM API request timed out")
            return "The AI service is slow to respond. Please try again shortly.", False
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "quota" in error_msg:
                logger.warning(f"LLM API rate limited: {e}")
                return "I'm receiving too many requests right now. Please wait a moment and try again.", False
            elif "api key" in error_msg or "authentication" in error_msg:
                logger.error(f"LLM API authentication error: {e}")
                return "There's a configuration issue with the AI service. Please contact support.", False
            else:
                logger.error(f"Error calling LLM API: {e}")
                return "I'm having trouble processing that request. Please try again.", False
