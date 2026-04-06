from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from integrations.calendar_service import CalendarService

from .base_agent import BaseAgent


class CalendarAgent(BaseAgent):
    id = "calendar_agent"
    name = "Calendar Agent"
    description = "Handles Google Calendar operations"
    capabilities = ["create", "view", "modify", "today_summary"]

    def __init__(self, calendar_service: CalendarService | None = None) -> None:
        self.calendar = calendar_service or CalendarService()

    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        if task == "today_summary":
            return {"success": True, "summary": self.calendar.get_today_summary()}

        if task == "list_events":
            events = self.calendar.get_events(max_results=params.get("max_results", 10))
            return {"success": True, "events": events}

        if task == "create_event":
            start = params.get("start")
            if isinstance(start, str):
                start_dt = datetime.fromisoformat(start)
            elif isinstance(start, datetime):
                start_dt = start
            else:
                start_dt = datetime.utcnow() + timedelta(hours=1)

            end = params.get("end")
            if isinstance(end, str):
                end_dt = datetime.fromisoformat(end)
            elif isinstance(end, datetime):
                end_dt = end
            else:
                end_dt = start_dt + timedelta(hours=1)

            return self.calendar.create_event(
                summary=params.get("summary", "Untitled Event"),
                start=start_dt,
                end=end_dt,
                description=params.get("description"),
                location=params.get("location"),
                attendees=params.get("attendees", []),
            )

        return {"success": False, "error": f"Unknown calendar task: {task}"}
