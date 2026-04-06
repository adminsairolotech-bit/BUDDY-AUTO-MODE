from __future__ import annotations

from typing import Any

import httpx

from .base_agent import BaseAgent


class SearchAgent(BaseAgent):
    id = "search_agent"
    name = "Search Agent"
    description = "Web search helper"
    capabilities = ["search"]

    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        if task != "search":
            return {"success": False, "error": f"Unknown search task: {task}"}
        query = params.get("query", "")
        if not query:
            return {"success": False, "error": "Missing query"}
        # Placeholder: no external provider key required.
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get("https://duckduckgo.com/", params={"q": query})
        return {"success": True, "query": query, "status_code": response.status_code}
