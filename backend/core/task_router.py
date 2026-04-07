from __future__ import annotations

from typing import Any

from agents.calendar_agent import CalendarAgent
from agents.desktop_agent import DesktopControlAgent
from agents.email_agent import EmailAgent
from agents.search_agent import SearchAgent
from agents.skill_agent import SkillAgent
from agents.telegram_agent import TelegramAgent


class TaskRouter:
    def __init__(
        self,
        email_agent: EmailAgent,
        telegram_agent: TelegramAgent,
        calendar_agent: CalendarAgent,
        desktop_agent: DesktopControlAgent,
        search_agent: SearchAgent,
        skill_agent: SkillAgent,
    ) -> None:
        self.email = email_agent
        self.telegram = telegram_agent
        self.calendar = calendar_agent
        self.desktop = desktop_agent
        self.search = search_agent
        self.skill = skill_agent

    async def route(self, intent: str, action: str, params: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        if intent == "email":
            task = "send_email" if action in {"send_email", "send"} else "read_email"
            return await self.email.execute(task, params, context)

        if intent == "telegram":
            return await self.telegram.execute("send_message", params, context)

        if intent == "calendar":
            task = action if action in {"today_summary", "create_event", "list_events"} else "list_events"
            return await self.calendar.execute(task, params, context)

        if intent == "desktop":
            desktop_action = params.get("action") or action or "open_app"
            return await self.desktop.execute(desktop_action, params, context)

        if intent in {"weather", "news", "calculator", "translator", "notes", "skill"}:
            skill_id = params.get("skill_id") or intent
            return await self.skill.execute("execute_skill", {"skill_id": skill_id, "params": params}, context)

        if intent == "search":
            return await self.search.execute("search", params, context)

        # Chat intent - return AI generated response text
        return {"success": True, "message": "Chat response processed.", "intent": intent, "echo": params}
