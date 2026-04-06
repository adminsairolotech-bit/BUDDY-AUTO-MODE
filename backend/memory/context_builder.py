from __future__ import annotations

from typing import Any

from .memory_manager import MemoryManager


class ContextBuilder:
    def __init__(self, user_id: str) -> None:
        self.memory = MemoryManager(user_id)

    async def build(self, conversation_id: str | None = None, command: str | None = None) -> dict[str, Any]:
        context = await self.memory.get_user_context()
        context["conversation_id"] = conversation_id
        context["current_input"] = command
        return context
