from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    id: str = "base_agent"
    name: str = "Base Agent"
    description: str = ""
    capabilities: list[str] = []

    @abstractmethod
    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError

    def metadata(self, status: str = "active") -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "status": status,
        }
