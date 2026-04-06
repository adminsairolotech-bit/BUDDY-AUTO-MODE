from __future__ import annotations

from typing import Any


class GitHubService:
    def __init__(self, token: str | None = None) -> None:
        self.token = token

    async def health(self) -> dict[str, Any]:
        return {"connected": bool(self.token)}
