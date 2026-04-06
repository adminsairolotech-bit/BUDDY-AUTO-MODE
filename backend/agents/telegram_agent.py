from __future__ import annotations

from typing import Any

from integrations.telegram_bot import TelegramBot

from .base_agent import BaseAgent


class TelegramAgent(BaseAgent):
    id = "telegram_agent"
    name = "Telegram Agent"
    description = "Handles Telegram messages"
    capabilities = ["send", "receive", "groups"]

    def __init__(self, bot: TelegramBot | None = None) -> None:
        self.bot = bot

    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        if task == "send_message":
            if not self.bot:
                return {"success": False, "error": "Telegram bot not configured"}
            await self.bot.send_message(chat_id=params.get("chat_id", ""), text=params.get("text", ""))
            return {"success": True, "message": "Message sent"}
        return {"success": False, "error": f"Unknown telegram task: {task}"}
