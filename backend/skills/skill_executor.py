from __future__ import annotations

from typing import Any

import httpx

from database.repositories import SkillRepository

from .skill_loader import SkillLoader


class SkillExecutor:
    def __init__(self, loader: SkillLoader) -> None:
        self.loader = loader
        self.repo = SkillRepository()

    async def execute(self, skill_id: str, params: dict[str, Any], user_id: str | None = None) -> dict[str, Any]:
        builtin = self.loader.get_builtin(skill_id)
        if builtin:
            result = await builtin(params, {"user_id": user_id} if user_id else None)
            return {"success": True, "result": result}

        if not user_id:
            return {"success": False, "error": "User context required for custom skill"}

        skill = await self.repo.get(user_id, skill_id)
        if not skill:
            return {"success": False, "error": f"Skill not found: {skill_id}"}

        actions = skill.get("actions", [])
        action_results = []
        for action in actions:
            action_type = action.get("type")
            if action_type == "api_call":
                output = await self._execute_api_call(action, params)
                action_results.append(output)
            else:
                action_results.append({"success": False, "error": f"Unsupported action: {action_type}"})

        template = skill.get("response_template") or "Skill executed."
        rendered = template
        for key, value in params.items():
            rendered = rendered.replace("{" + key + "}", str(value))

        return {"success": True, "result": {"text": rendered, "actions": action_results}}

    async def _execute_api_call(self, action: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
        config = action.get("config", {})
        url = action.get("url") or config.get("url")
        method = (action.get("method") or config.get("method") or "GET").upper()
        if not url:
            return {"success": False, "error": "Missing API URL"}

        query_params = config.get("params", {})
        compiled = {k: self._render(v, params) for k, v in query_params.items()}
        async with httpx.AsyncClient(timeout=15) as client:
            try:
                response = await client.request(method, self._render(url, params), params=compiled)
                return {"success": response.status_code < 400, "status_code": response.status_code, "body": response.text[:2000]}
            except Exception as exc:
                return {"success": False, "error": str(exc)}

    @staticmethod
    def _render(value: Any, params: dict[str, Any]) -> Any:
        if isinstance(value, str):
            out = value
            for key, param in params.items():
                out = out.replace("{" + key + "}", str(param))
            return out
        return value
