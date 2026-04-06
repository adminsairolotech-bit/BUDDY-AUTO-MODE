from __future__ import annotations

from typing import Any

from skills.skill_executor import SkillExecutor

from .base_agent import BaseAgent


class SkillAgent(BaseAgent):
    id = "skill_agent"
    name = "Skill Agent"
    description = "Executes built-in and custom skills"
    capabilities = ["execute_skill"]

    def __init__(self, executor: SkillExecutor) -> None:
        self.executor = executor

    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        if task != "execute_skill":
            return {"success": False, "error": f"Unknown skill task: {task}"}
        skill_id = params.get("skill_id")
        if not skill_id:
            return {"success": False, "error": "skill_id is required"}
        return await self.executor.execute(skill_id=skill_id, params=params.get("params", {}), user_id=(context or {}).get("user_id"))
