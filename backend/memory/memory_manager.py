from __future__ import annotations

from typing import Any

from database.repositories import ConversationRepository, MemoryRepository
from utils.sanitizers import contains_sensitive_content, sanitize_memory_value


class MemoryManager:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.memory_repo = MemoryRepository()
        self.conv_repo = ConversationRepository()

    async def store_memory(self, memory_type: str, key: str, value: Any, context: str | None = None, confidence: float = 1.0) -> str:
        sanitized_value, redacted = sanitize_memory_value(key, value)
        final_context = context
        if redacted and context:
            final_context = "[REDACTED_SENSITIVE_CONTEXT]"
        return await self.memory_repo.upsert(self.user_id, memory_type, key, sanitized_value, final_context, confidence)

    async def get_memory(self, key: str) -> dict[str, Any] | None:
        return await self.memory_repo.get(self.user_id, key)

    async def search_memory(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        return await self.memory_repo.search(self.user_id, query, limit)

    async def get_user_context(self) -> dict[str, Any]:
        user_info_items = await self.memory_repo.by_type(self.user_id, "user_info")
        pref_items = await self.memory_repo.by_type(self.user_id, "preference")
        patterns = await self.memory_repo.by_type(self.user_id, "learned_pattern", limit=20)
        latest_conv = await self.conv_repo.latest_for_user(self.user_id)

        user_info = {m["key"]: m.get("value") for m in user_info_items}
        preferences = {m["key"]: m.get("value") for m in pref_items}
        top_patterns = [
            {"pattern": m.get("key"), "value": m.get("value")}
            for m in sorted(patterns, key=lambda x: x.get("access_count", 0), reverse=True)[:5]
        ]

        return {
            "user_info": user_info,
            "preferences": preferences,
            "recent_conversation": (latest_conv or {}).get("summary"),
            "learned_patterns": top_patterns,
        }

    async def learn_from_interaction(self, command: str, intent: str, params: dict[str, Any], feedback: str = "correct") -> None:
        if feedback != "correct":
            return
        safe_params = {k: ("[REDACTED_SENSITIVE]" if contains_sensitive_content(k, v) else v) for k, v in params.items()}
        key = f"intent_{intent}"
        existing = await self.get_memory(key)
        examples = []
        if existing and isinstance(existing.get("value"), dict):
            examples = existing["value"].get("examples", [])
        safe_command = "[REDACTED_SENSITIVE_COMMAND]" if contains_sensitive_content("command", command) else command
        examples.append({"command": safe_command, "params": safe_params})
        examples = examples[-10:]
        await self.store_memory("learned_pattern", key, {"intent": intent, "examples": examples}, "Auto-learned from command")

    async def delete_memory(self, key: str) -> bool:
        return await self.memory_repo.delete(self.user_id, key)

    async def delete_all_memory(self) -> int:
        return await self.memory_repo.delete_all(self.user_id)

    async def delete_conversation(self, conversation_id: str) -> bool:
        return await self.conv_repo.delete_conversation(self.user_id, conversation_id)

    async def forget_me(self) -> dict[str, int]:
        memory_deleted = await self.memory_repo.delete_all(self.user_id)
        conversations_deleted = await self.conv_repo.delete_all_for_user(self.user_id)
        return {"memory_deleted": memory_deleted, "conversations_deleted": conversations_deleted}
