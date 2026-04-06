from __future__ import annotations

from typing import Any

from .base_agent import BaseAgent


class DesktopControlAgent(BaseAgent):
    id = "desktop_agent"
    name = "Desktop Agent"
    description = "Controls desktop computer via websocket bridge"
    capabilities = ["apps", "files", "browser", "keyboard", "mouse", "command"]

    def __init__(self, desktop_dispatcher: Any) -> None:
        self.desktop_dispatcher = desktop_dispatcher

    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        # task is treated as action for desktop agent.
        response = await self.desktop_dispatcher.send_task(
            user_id=(context or {}).get("user_id", ""),
            action=task,
            params=params,
        )
        return response
